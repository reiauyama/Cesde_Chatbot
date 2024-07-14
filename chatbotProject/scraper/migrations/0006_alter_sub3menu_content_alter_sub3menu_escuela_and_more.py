# Generated by Django 5.0.7 on 2024-07-14 20:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_alter_sub3menu_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub3menu',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='sub3menu',
            name='escuela',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sub3menu',
            name='link',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='sub3menu',
            name='subsubmenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.subsubmenu'),
        ),
        migrations.AlterUniqueTogether(
            name='sub3menu',
            unique_together={('subsubmenu', 'escuela')},
        ),
    ]
