# Generated by Django 5.1 on 2025-02-11 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("items", "0011_item_ai_generated_json"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="item",
            name="item_keyword",
        ),
    ]
