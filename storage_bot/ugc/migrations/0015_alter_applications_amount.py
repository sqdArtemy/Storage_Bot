# Generated by Django 3.2.7 on 2021-10-12 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0014_remove_applications_counter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='amount',
            field=models.FloatField(verbose_name='Количество'),
        ),
    ]