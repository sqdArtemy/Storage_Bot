# Generated by Django 3.2.7 on 2021-10-12 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0013_applications_counter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applications',
            name='counter',
        ),
    ]
