# Generated by Django 3.2.7 on 2021-10-15 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0018_profile_change_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='change_amount',
            field=models.TextField(default=0, verbose_name='Количество для изменения'),
        ),
    ]
