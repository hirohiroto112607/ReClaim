# Generated by Django 5.1 on 2025-02-15 01:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="item_category",
            fields=[
                ("category_id", models.AutoField(primary_key=True, serialize=False)),
                ("category_name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="item",
            fields=[
                ("item_id", models.AutoField(primary_key=True, serialize=False)),
                ("item_name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "item_date",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "item_lost_location",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("item_description", models.TextField(blank=True, null=True)),
                (
                    "item_image",
                    models.ImageField(blank=True, null=True, upload_to="images/"),
                ),
                ("item_status", models.BooleanField(default=False)),
                ("ai_generated_json", models.TextField(blank=True, null=True)),
                (
                    "item_founder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "item_category_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="items.item_category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="item_message",
            fields=[
                ("message_id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField(max_length=500)),
                (
                    "item_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="items.item"
                    ),
                ),
            ],
        ),
    ]
