# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-14 13:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180614_1251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailverifyrecord',
            options={'verbose_name': 'email_verifycode', 'verbose_name_plural': 'email_verifycode'},
        ),
    ]
