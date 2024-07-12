# Generated by Django 5.0.7 on 2024-07-12 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submenu',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.CreateModel(
            name='sub3menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('escuela', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('subsubmenu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub3menus', to='scraper.subsubmenu')),
            ],
        ),
    ]
