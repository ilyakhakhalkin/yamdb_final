# Generated by Django 2.2.16 on 2022-10-06 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20221006_1103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
    ]
