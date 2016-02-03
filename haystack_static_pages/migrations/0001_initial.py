# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('url', models.CharField(max_length=255, null=True, verbose_name='url', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('content', models.TextField(verbose_name='content')),
                ('language', models.CharField(max_length=5, null=True, verbose_name='language', blank=True)),
            ],
            options={
                'verbose_name': 'static page',
                'verbose_name_plural': 'static pages',
            },
        ),
    ]
