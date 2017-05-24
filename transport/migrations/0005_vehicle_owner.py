# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 14:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0004_auto_20170523_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='transport.SiteUser'),
            preserve_default=False,
        ),
    ]