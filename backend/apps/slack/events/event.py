"""Base class and common functionality for Slack events."""

import logging
from collections.abc import Callable
from typing import Any

from django.conf import settings
from slack_sdk.errors import SlackApiError

from apps.common.constants import NL
from apps.common.utils import convert_to_snake_case
from apps.slack.apps import SlackConfig
from apps.slack.blocks import markdown
from apps.slack.template_loader import env
from apps.slack.utils import get_text

logger = logging.getLogger(__name__)


class EventBase:
    """Base class for Slack events with common functionality.

    Template formatting notes:
        - Use "{{ SECTION_BREAK }}" to separate content into different Slack blocks
        - Use "{{ DIVIDER }}" to insert a horizontal divider
    """

    event_type: str | None = None
    matchers: list[Callable[[Any], bool]] | None = None

    @staticmethod
    def configure_events():
        """Configure all event handlers with the Slack app."""
        if SlackConfig.app is None:
            logger.warning("SlackConfig.app is None. Event handlers are not registered.")
            return

        for event_class in EventBase.get_events():
            event_class().register()

    @staticmethod
    def get_events():
        """Yield all subclasses of EventBase."""
        yield from EventBase.__subclasses__()

    @property
    def ephemeral_message(self) -> tuple | None:
        """Return ephemeral message text."""
        return None

    def register(self):
        """Register this event handler with the Slack app."""
        SlackConfig.app.event(
            self.event_type,
            matchers=self.matchers,
        )(self.handler)

    def handler(self, event, client, ack):
        """Handle the Slack event.

        Args:
            event (dict): The Slack event payload.
            client (WebClient): The Slack WebClient instance.
            ack (Callable): Function to acknowledge the event.

        """
        ack()

        if not settings.SLACK_EVENTS_ENABLED:
            return

        try:
            self.handle_event(event, client)
        except SlackApiError as e:
            if e.response["error"] == "cannot_dm_bot":
                logger.warning("Cannot DM bot user in event %s", self.event_type)
                return
            raise
        except Exception:
            logger.exception("Error handling %s", self.event_type)

    def handle_event(self, event, client):
        """Implement event handling logic.

        Args:
            event (dict): The Slack event payload.
            client (WebClient): The Slack WebClient instance.

        """
        user_id = self.get_user_id(event)

        if (blocks := self.get_render_blocks(self.get_context(event))) and (
            conversation := self.open_conversation(client, user_id)
        ):
            client.chat_postMessage(
                blocks=blocks,
                channel=conversation["channel"]["id"],
                text=get_text(blocks),
            )

        if ephemeral_message := self.ephemeral_message:
            client.chat_postEphemeral(
                blocks=ephemeral_message,
                channel=event["channel"],
                text=get_text(ephemeral_message),
                user=user_id,
            )

    def open_conversation(self, client, user_id):
        """Open a DM conversation with a user.

        Args:
            client (WebClient): The Slack WebClient instance.
            user_id (str): The Slack user ID.

        Returns:
            dict or None: The conversation object, or None if cannot DM bot.

        """
        if not user_id:
            return None

        try:
            return client.conversations_open(users=user_id)
        except SlackApiError as e:
            if e.response["error"] == "cannot_dm_bot":
                return None
            raise

    def get_render_blocks(self, context):
        """Render Slack blocks from the template using the provided context.

        Args:
            context (dict): The context for template rendering.

        Returns:
            list: List of Slack block objects.

        """
        blocks = []
        for section in self.get_render_text(context).split("{{ SECTION_BREAK }}"):
            if section.strip() == "{{ DIVIDER }}":
                blocks.append({"type": "divider"})
            elif section:
                blocks.append(markdown(section))

        return blocks

    def get_render_text(self, context):
        """Render the template as plain text using the provided context.

        Args:
            context (dict): The context for template rendering.

        Returns:
            str: The rendered text.

        """
        return self.get_template_file().render(
            **self.get_template_context(context),
        )

    def get_template_context(self, context):
        """Build the template context, including base variables and the provided context.

        Args:
            context (dict): The event- or handler-specific context.

        Returns:
            dict: The complete context for template rendering.

        """
        return {
            "DIVIDER": "{{ DIVIDER }}",
            "NL": NL,
            "SECTION_BREAK": "{{ SECTION_BREAK }}",
            **context,
        }

    def get_template_file(self):
        """Get the Jinja template file for this event handler.

        Returns:
            Template: The Jinja template object.

        """
        return env.get_template(self.get_template_file_name())

    def get_template_file_name(self):
        """Get the template file name for this event handler.

        Returns:
            str: The template file name in snake_case.

        """
        return f"events/{convert_to_snake_case(self.__class__.__name__)}.jinja"

    def get_user_id(self, event) -> str:
        """Get the user ID from the event.

        Args:
            event (dict): The Slack event payload.

        Returns:
            str: The user ID.

        """
        return event["user"]
