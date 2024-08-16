# Generated by Django 5.1 on 2024-08-16 01:42

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Repository",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "description",
                    models.CharField(default="", max_length=500, verbose_name="Description"),
                ),
                ("is_archived", models.BooleanField(default=False, verbose_name="Is archived")),
                ("is_fork", models.BooleanField(default=False, verbose_name="Is fork")),
                (
                    "forks_count",
                    models.PositiveIntegerField(default=0, verbose_name="Forks count"),
                ),
                (
                    "open_issues_count",
                    models.PositiveIntegerField(default=0, verbose_name="Open issues count"),
                ),
                (
                    "stars_count",
                    models.PositiveIntegerField(default=0, verbose_name="Stars count"),
                ),
                (
                    "subscribers_count",
                    models.PositiveIntegerField(default=0, verbose_name="Subscribers count"),
                ),
                ("language", models.CharField(default="", max_length=50, verbose_name="Language")),
                ("size", models.PositiveIntegerField(default=0, verbose_name="Size in KB")),
                (
                    "platform",
                    models.CharField(
                        choices=[("github", "GitHub")],
                        default="github",
                        max_length=10,
                        verbose_name="Platform",
                    ),
                ),
                (
                    "platform_created_at",
                    models.DateTimeField(verbose_name="Platform creation time"),
                ),
                (
                    "platform_pushed_at",
                    models.DateTimeField(verbose_name="Platform last push time"),
                ),
                (
                    "platform_update_at",
                    models.DateTimeField(verbose_name="Platform last update time"),
                ),
                ("owner_login", models.CharField(max_length=100, verbose_name="Owner login")),
                (
                    "owner_type",
                    models.CharField(
                        choices=[("organization", "Organization"), ("user", "User")],
                        default="user",
                        max_length=20,
                        verbose_name="Owner type",
                    ),
                ),
            ],
            options={
                "db_table": "repositories",
                "constraints": [
                    models.UniqueConstraint(
                        fields=("name", "platform"), name="unique_name_platform"
                    )
                ],
            },
        ),
    ]
