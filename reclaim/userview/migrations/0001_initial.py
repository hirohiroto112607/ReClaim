# Generated by Django 5.1 on 2024-12-19 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=254)),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
            ],
        ),
    ]
