# Generated by Django 5.0.6 on 2024-06-11 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stackusers', '0006_rename_date_earned_userbadge_date_awarded_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbadge',
            name='badge',
        ),
        migrations.RemoveField(
            model_name='userbadge',
            name='user',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Badge',
        ),
        migrations.DeleteModel(
            name='UserBadge',
        ),
    ]
