# Generated by Django 5.1 on 2025-01-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("items", "0003_alter_item_item_category_id_alter_item_item_tag_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="item",
            name="item_tag_id",
        ),
        migrations.AddField(
            model_name="item",
            name="item_tag_id",
            field=models.ManyToManyField(to="items.tag"),
        ),
    ]
