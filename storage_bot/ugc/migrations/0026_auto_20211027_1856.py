# Generated by Django 3.2.7 on 2021-10-27 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0025_alter_applications_storage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='company',
            field=models.TextField(default='samples', verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='storage',
            field=models.TextField(default='sample', verbose_name='Склад'),
        ),
    ]
