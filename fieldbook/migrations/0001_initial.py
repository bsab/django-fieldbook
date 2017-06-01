# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 08:27
from __future__ import unicode_literals

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
            name='FieldBookUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fieldbook_api_key', models.CharField(default='', max_length=55)),
                ('fieldbook_api_secret', models.CharField(default='', max_length=55)),
                ('fieldbook_book', models.CharField(default='', max_length=55)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
