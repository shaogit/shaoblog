# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-17 10:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0008_auto_20170917_1741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='blog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog'),
            preserve_default=False,
        ),
    ]
