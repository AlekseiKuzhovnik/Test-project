# Generated by Django 4.1.1 on 2023-01-02 13:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_weather'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
