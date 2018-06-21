# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-19 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=100, verbose_name='chapter_name'),
        ),
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('entry', 'entry_level'), ('intermediate', 'mid_level'), ('advanced', 'advanced_level')], max_length=2, verbose_name='course_degree'),
        ),
    ]