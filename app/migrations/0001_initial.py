# Generated by Django 5.0.1 on 2024-03-16 14:05

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CompanyInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(blank=True, null=True)),
                ("video", models.FileField(blank=True, upload_to="files/")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="images/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["ico", "png", "jpeg", "jpg"],
                                message="Enter an image in the format below('ico','png','jpeg','jpg')",
                            )
                        ],
                    ),
                ),
                ("add_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="CompanyStructure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(blank=True, null=True)),
                ("video", models.FileField(blank=True, upload_to="files/")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="images/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["ico", "png", "jpeg", "jpg"],
                                message="Enter an image in the format below('ico','png','jpeg','jpg')",
                            )
                        ],
                    ),
                ),
                ("add_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(default=False)),
                (
                    "position",
                    models.CharField(
                        choices=[
                            ("admin", "Admin"),
                            ("manager", "Manager"),
                            ("worker", "Ishchi"),
                            ("student", "Shogird"),
                        ],
                        default="worker",
                        help_text="Choose positions",
                        max_length=55,
                        verbose_name="Enter the position",
                    ),
                ),
                (
                    "full_name",
                    models.CharField(max_length=155, verbose_name="Enter the name"),
                ),
                (
                    "phone_number",
                    models.CharField(
                        max_length=20, verbose_name="Enter the phone number"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="images/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["ico", "png", "jpeg", "jpg"],
                                message="Enter an image in the format below('ico','png','jpeg','jpg')",
                            )
                        ],
                    ),
                ),
                ("add_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="TelegramUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(blank=True, max_length=40, null=True)),
                (
                    "telegram_id",
                    models.CharField(max_length=10, verbose_name="Telegram_ID"),
                ),
                ("add_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Complaint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("desc", models.TextField(blank=True, verbose_name="Enter the task !")),
                ("add_date", models.DateTimeField(auto_now_add=True)),
                (
                    "employees",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.employee"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("add_date", models.DateTimeField(auto_now_add=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.employee"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Advance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("desc", models.TextField(blank=True, verbose_name="Enter the task !")),
                ("amount", models.BigIntegerField(verbose_name="Amount")),
                ("add_date", models.DateTimeField(auto_now_add=True)),
                (
                    "employees",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.employee"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("desc", models.TextField(blank=True, verbose_name="Enter the task !")),
                ("add_date", models.DateTimeField(auto_now_add=True)),
                (
                    "employees",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.employee"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "task_status",
                    models.CharField(
                        choices=[
                            ("active", "Aktiv"),
                            ("progress", "Jarayonda"),
                            ("done", "Bajarildi"),
                        ],
                        default="active",
                        help_text="Choose status",
                        max_length=15,
                        verbose_name="Enter the status",
                    ),
                ),
                ("name", models.TextField(verbose_name="Enter the task !")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="images/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["ico", "png", "jpeg", "jpg"],
                                message="Enter an image in the format below('ico','png','jpeg','jpg')",
                            )
                        ],
                    ),
                ),
                ("add_date", models.DateTimeField(auto_now_add=True)),
                (
                    "accepted",
                    models.ManyToManyField(
                        blank=True, related_name="tasks_accepted", to="app.employee"
                    ),
                ),
                (
                    "employees",
                    models.ManyToManyField(
                        blank=True,
                        limit_choices_to={
                            "position__in": ["manager", "worker", "student"]
                        },
                        related_name="tasks_assigned",
                        to="app.employee",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="employee",
            name="telegram_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="employees",
                to="app.telegramuser",
            ),
        ),
    ]
