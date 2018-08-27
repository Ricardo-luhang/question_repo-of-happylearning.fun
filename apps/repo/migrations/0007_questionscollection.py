# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-24 16:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repo', '0006_questions_answer_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionsCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='收藏/取消时间')),
                ('status', models.BooleanField(default=True, verbose_name='收藏状态')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_collection_set', to='repo.Questions', verbose_name='问题')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_collection_set', to=settings.AUTH_USER_MODEL, verbose_name='收藏者')),
            ],
            options={
                'verbose_name': '收藏记录',
                'verbose_name_plural': '收藏记录',
            },
        ),
    ]
