# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-08 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram_id', models.CharField(max_length=50)),
                ('media_type', models.PositiveSmallIntegerField(choices=[(0, b'image'), (1, b'video')])),
                ('username', models.CharField(max_length=50)),
                ('caption', models.TextField()),
                ('created_time', models.DateTimeField(null=True)),
                ('url', models.URLField()),
                ('low_resolution_url', models.URLField()),
            ],
            options={
                'ordering': ('-created_time',),
            },
        ),
    ]
