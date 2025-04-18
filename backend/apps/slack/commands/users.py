"""Slack bot users command."""

from django.conf import settings

from apps.slack.apps import SlackConfig
from apps.slack.common.handlers.users import get_blocks
from apps.slack.common.presentation import EntityPresentation
from apps.slack.utils import get_text

COMMAND = "/users"


def users_handler(ack, command, client):
    """Handle the Slack /users command.

    Args:
        ack (function): Acknowledge the Slack command request.
        command (dict): The Slack command payload.
        client (slack_sdk.WebClient): The Slack WebClient instance for API calls.

    """
    ack()

    if not settings.SLACK_COMMANDS_ENABLED:
        return

    search_query = command["text"].strip()

    blocks = get_blocks(
        search_query=search_query,
        limit=10,
        presentation=EntityPresentation(
            include_feedback=True,
            include_metadata=True,
            include_pagination=False,
            include_timestamps=True,
            name_truncation=80,
            summary_truncation=300,
        ),
    )

    conversation = client.conversations_open(users=command["user_id"])
    client.chat_postMessage(
        blocks=blocks,
        channel=conversation["channel"]["id"],
        text=get_text(blocks),
    )


if SlackConfig.app:
    users_handler = SlackConfig.app.command(COMMAND)(users_handler)
