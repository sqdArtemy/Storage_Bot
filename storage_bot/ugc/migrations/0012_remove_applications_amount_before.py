# Generated by Django 3.2.7 on 2021-10-09 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0011_applications_amount_before'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applications',
            name='amount_before',
        ),
    ]
