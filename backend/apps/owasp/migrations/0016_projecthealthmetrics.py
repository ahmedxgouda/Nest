# Generated by Django 5.1.6 on 2025-02-28 11:57

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("owasp", "0015_snapshot"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectHealthMetrics",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("nest_created_at", models.DateTimeField(auto_now_add=True)),
                ("nest_updated_at", models.DateTimeField(auto_now=True)),
                (
                    "contributors_count",
                    models.PositiveIntegerField(default=0, verbose_name="Contributors"),
                ),
                (
                    "created_at",
                    models.DateTimeField(blank=True, null=True, verbose_name="Created at"),
                ),
                ("forks_count", models.PositiveIntegerField(default=0, verbose_name="Forks")),
                (
                    "is_funding_requirements_compliant",
                    models.BooleanField(
                        default=False, verbose_name="Is funding requirements compliant"
                    ),
                ),
                (
                    "is_project_leaders_requirements_compliant",
                    models.BooleanField(
                        default=False, verbose_name="Is project leaders requirements compliant"
                    ),
                ),
                (
                    "last_released_at",
                    models.DateTimeField(blank=True, null=True, verbose_name="Last released at"),
                ),
                (
                    "last_committed_at",
                    models.DateTimeField(blank=True, null=True, verbose_name="Last committed at"),
                ),
                (
                    "open_issues_count",
                    models.PositiveIntegerField(default=0, verbose_name="Open issues"),
                ),
                (
                    "open_pull_requests_count",
                    models.PositiveIntegerField(default=0, verbose_name="Open pull requests"),
                ),
                (
                    "owasp_page_last_updated_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="OWASP page last updated at"
                    ),
                ),
                (
                    "pull_request_last_created_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Pull request last created at"
                    ),
                ),
                (
                    "recent_releases_count",
                    models.PositiveIntegerField(default=0, verbose_name="Recent releases"),
                ),
                (
                    "score",
                    models.FloatField(
                        default=0.0,
                        help_text="Project health score (0-100)",
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(100.0),
                        ],
                    ),
                ),
                ("stars_count", models.PositiveIntegerField(default=0, verbose_name="Stars")),
                (
                    "total_issues_count",
                    models.PositiveIntegerField(default=0, verbose_name="Total issues"),
                ),
                (
                    "total_pull_request_count",
                    models.PositiveIntegerField(default=0, verbose_name="Total pull requests"),
                ),
                (
                    "total_releases_count",
                    models.PositiveIntegerField(default=0, verbose_name="Total releases"),
                ),
                (
                    "unanswered_issues_count",
                    models.PositiveIntegerField(default=0, verbose_name="Unanswered issues"),
                ),
                (
                    "unassigned_issues_count",
                    models.PositiveIntegerField(default=0, verbose_name="Unassigned issues"),
                ),
                (
                    "project",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="health_metrics",
                        to="owasp.project",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Project Health Metrics",
                "db_table": "owasp_project_health_metrics",
            },
        ),
    ]
