# Generated by Django 5.0.6 on 2024-06-12 09:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackbase', '0007_badge_badge_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='answers',
            field=models.ManyToManyField(related_name='badge_answers', to='stackbase.answer'),
        ),
        migrations.AddField(
            model_name='badge',
            name='bronze_badges_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='badge',
            name='gold_badges_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='badge',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='badge',
            name='questions',
            field=models.ManyToManyField(related_name='badge_questions', to='stackbase.question'),
        ),
        migrations.AddField(
            model_name='badge',
            name='silver_badges_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='badge',
            name='users',
            field=models.ManyToManyField(related_name='badges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='level_image',
            field=models.ImageField(default='Standard', upload_to='level_images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='badge',
            name='badge_type',
            field=models.CharField(choices=[('Gold', 'Gold'), ('Silver', 'Silver'), ('Bronze', 'Bronze')], max_length=6),
        ),
        migrations.AlterField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='stackbase.question'),
        ),
    ]
