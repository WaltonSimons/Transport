# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0006_offerbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerbid',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
