# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-25 21:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('course', '0002_auto_20180619_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(blank='True', null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='course_organization'),
        ),
    ]
