# Generated by Django 2.2.16 on 2022-10-06 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20221005_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Genre')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Title')),
            ],
        ),
    ]