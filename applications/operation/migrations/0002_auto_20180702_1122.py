# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-02 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_type',
            field=models.IntegerField(choices=[(1, 'Course'), (2, 'Organization'), (3, 'Teacher')], default=1, verbose_name='fav_type'),
        ),
    ]
