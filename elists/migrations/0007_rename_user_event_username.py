# Generated by Django 4.1.1 on 2023-01-06 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elists', '0006_event_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='user',
            new_name='username',
        ),
    ]
