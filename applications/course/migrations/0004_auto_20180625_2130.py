# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-25 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_course_course_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('entry', 'entry_level'), ('intermediate', 'mid_level'), ('advanced', 'advanced_level')], max_length=20, verbose_name='course_degree'),
        ),
    ]