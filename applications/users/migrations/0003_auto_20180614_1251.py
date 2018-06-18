# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-14 12:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_banner_emailverifyrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='female', max_length=10),
        ),
    ]
