# Generated by Django 3.2.11 on 2023-04-26 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_thread_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='post',
        ),
    ]
