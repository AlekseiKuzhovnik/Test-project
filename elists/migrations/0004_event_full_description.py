# Generated by Django 4.1.1 on 2023-01-02 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elists', '0003_alter_event_event_creator_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='full_description',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]