# Generated by Django 3.2.7 on 2021-11-01 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0031_auto_20211101_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_page',
            field=models.IntegerField(default=0, verbose_name='Действующая страница'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='previous_page',
            field=models.IntegerField(default=0, verbose_name='Предыдущая страница'),
        ),
    ]
