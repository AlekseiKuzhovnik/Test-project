# Generated by Django 4.1.1 on 2022-12-30 11:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('city', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('degree', models.IntegerField()),
                ('icon_name', models.CharField(max_length=20)),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
