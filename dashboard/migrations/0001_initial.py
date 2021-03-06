# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-01 21:18
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Estacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estacion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homeopatia', models.BooleanField(default=False)),
                ('nombre_comercial', models.CharField(default='-', max_length=150)),
                ('nombre_generico', models.CharField(default='-', max_length=150)),
                ('cantidad_frasco', models.CharField(default='N/A', max_length=50)),
                ('dosis', models.CharField(default='-', max_length=20)),
                ('formato_medicamento', models.CharField(default='-', max_length=50)),
                ('tipo_medicamento', models.CharField(default='-', max_length=100)),
                ('descripcion', models.TextField(default='-')),
            ],
        ),
        migrations.CreateModel(
            name='Medicamento_Ubicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Medicamento')),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now)),
                ('salida', models.BooleanField()),
                ('descripcion_tipo', models.CharField(blank=True, max_length=150, null=True)),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destino', to='dashboard.Estacion')),
                ('origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origen', to='dashboard.Estacion')),
            ],
        ),
        migrations.CreateModel(
            name='Orden_Medicamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('fecha_vencimiento', models.DateField()),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Medicamento')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Orden')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
                ('clase', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubicacion', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='orden',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Tipo_Orden'),
        ),
        migrations.AddField(
            model_name='orden',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medicamento_ubicacion',
            name='ubicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Ubicacion'),
        ),
    ]
