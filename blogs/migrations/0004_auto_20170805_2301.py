# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_auto_20170805_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img',
            field=models.ImageField(upload_to='blogs/static/blogs/img'),
        ),
    ]
