# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-02 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20180625_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='Back-End', max_length=20, verbose_name='course_category'),
        ),
    ]
