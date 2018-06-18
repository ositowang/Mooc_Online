# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-13 16:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('image', models.ImageField(upload_to='banner/%Y/%m', verbose_name='banner_image')),
                ('url', models.URLField(verbose_name='image_url')),
                ('index', models.IntegerField(default=100, verbose_name='image_sequence')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add_time')),
            ],
            options={
                'verbose_name': 'banner',
                'verbose_name_plural': 'banner',
            },
        ),
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='verify_code')),
                ('email', models.EmailField(max_length=50, verbose_name='user_email')),
                ('send_type', models.CharField(choices=[('register', 'new_user'), ('forget', 'forget_password')], max_length=10)),
                ('send_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'email_verify_code',
                'verbose_name_plural': 'email_verify_code',
            },
        ),
    ]
