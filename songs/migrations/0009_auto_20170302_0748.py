# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0008_auto_20170301_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='dislike_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='like_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='view_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]