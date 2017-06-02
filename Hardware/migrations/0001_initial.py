# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=32, verbose_name=b'IP\xe5\x9c\xb0\xe5\x9d\x80')),
                ('hostname', models.CharField(max_length=32, verbose_name=b'\xe4\xb8\xbb\xe6\x9c\xba\xe5\x90\x8d')),
                ('mac', models.CharField(max_length=32, verbose_name=b'MAC')),
                ('manu', models.CharField(max_length=16, verbose_name=b'\xe7\xa1\xac\xe4\xbb\xb6\xe5\x8e\x82\xe5\x95\x86')),
                ('code', models.CharField(max_length=32, verbose_name=b'\xe8\xb5\x84\xe4\xba\xa7\xe7\xbc\x96\xe5\x8f\xb7')),
                ('os', models.CharField(max_length=32, verbose_name=b'\xe7\xb3\xbb\xe7\xbb\x9f')),
                ('idc', models.CharField(max_length=32, verbose_name=b'\xe6\x9c\xba\xe6\x88\xbf')),
                ('sn', models.CharField(max_length=32, verbose_name=b'SN\xe7\xbc\x96\xe5\x8f\xb7')),
                ('description', models.TextField(null=True, verbose_name=b'\xe7\xa1\xac\xe4\xbb\xb6\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
            ],
        ),
    ]
