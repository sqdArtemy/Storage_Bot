# Generated by Django 3.2.7 on 2021-10-28 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0026_auto_20211027_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='selected_company',
        ),
    ]
