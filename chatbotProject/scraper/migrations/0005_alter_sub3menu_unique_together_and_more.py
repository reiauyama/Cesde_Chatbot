# Generated by Django 5.0.7 on 2024-07-14 20:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_alter_sub3menu_content_alter_sub3menu_escuela_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sub3menu',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='sub3menu',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sub3menu',
            name='escuela',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='sub3menu',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sub3menu',
            name='subsubmenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub3menus', to='scraper.subsubmenu'),
        ),
    ]
