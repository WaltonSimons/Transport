# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0002_siteuser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteuser',
            name='driver',
        ),
        migrations.AddField(
            model_name='siteuser',
            name='name',
            field=models.TextField(default='Jan', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='siteuser',
            name='phone_number',
            field=models.TextField(default='', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='siteuser',
            name='surname',
            field=models.TextField(default='Nowak', max_length=255),
            preserve_default=False,
        ),
    ]
