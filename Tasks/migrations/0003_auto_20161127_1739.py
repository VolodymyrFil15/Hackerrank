# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-27 17:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tasks', '0002_auto_20161127_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='path',
            new_name='task_text',
        ),
    ]
