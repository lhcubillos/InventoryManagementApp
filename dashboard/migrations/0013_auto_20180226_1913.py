# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-26 22:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_tipo_orden_clase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='tipo_usuario',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
