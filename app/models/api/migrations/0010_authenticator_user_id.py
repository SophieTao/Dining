# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-19 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20170319_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='authenticator',
            name='user_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
