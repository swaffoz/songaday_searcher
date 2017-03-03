# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 07:55
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0007_auto_20170301_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='url',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]