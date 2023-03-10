# Generated by Django 4.1.1 on 2023-01-02 15:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('short_description', models.CharField(max_length=200, null=True)),
                ('event_creator_id', models.CharField(max_length=20)),
                ('create_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('is_closed', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='EventUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
