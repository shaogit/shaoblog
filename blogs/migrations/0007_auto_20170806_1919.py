# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_auto_20170806_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='push_image',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='push_style',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
