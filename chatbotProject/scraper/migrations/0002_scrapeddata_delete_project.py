# Generated by Django 5.0.7 on 2024-07-10 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
