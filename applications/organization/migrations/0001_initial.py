# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-13 16:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='city_name')),
                ('desc', models.CharField(max_length=200, verbose_name='city_desc')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'city',
            },
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='organization_name')),
                ('desc', models.TextField(verbose_name='organization_desc')),
                ('click_num', models.IntegerField(default=0, verbose_name='click_num')),
                ('fav_num', models.IntegerField(default=0, verbose_name='fav_num')),
                ('image', models.ImageField(upload_to='org/%Y/%m', verbose_name='organization_cover_image')),
                ('address', models.CharField(max_length=150, verbose_name='organization_address')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CityDict', verbose_name='organization_city')),
            ],
            options={
                'verbose_name': 'course_organization',
                'verbose_name_plural': 'course_organization',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='teacher_name')),
                ('work_years', models.IntegerField(default=0, verbose_name='work_years')),
                ('company', models.CharField(max_length=50, verbose_name='teacher_company')),
                ('work_position', models.CharField(max_length=50, verbose_name='teacher_position')),
                ('advantages', models.CharField(max_length=50, verbose_name='teacher_advantage')),
                ('click_num', models.IntegerField(default=0, verbose_name='click_num')),
                ('fav_num', models.IntegerField(default=0, verbose_name='fav_num')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='teacher_organization')),
            ],
            options={
                'verbose_name': 'teacher',
                'verbose_name_plural': 'teacher',
            },
        ),
    ]