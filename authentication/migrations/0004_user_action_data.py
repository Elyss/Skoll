# Generated by Django 4.2.6 on 2023-10-17 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='action_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
