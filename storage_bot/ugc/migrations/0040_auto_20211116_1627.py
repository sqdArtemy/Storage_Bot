# Generated by Django 3.2.7 on 2021-11-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0039_application_callback_stat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application_callback',
            name='appl',
        ),
        migrations.RemoveField(
            model_name='application_callback',
            name='stat',
        ),
        migrations.AddField(
            model_name='application_callback',
            name='app_id',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Application status'),
            preserve_default=False,
        ),
    ]
