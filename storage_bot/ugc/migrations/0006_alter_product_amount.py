# Generated by Django 3.2.7 on 2021-09-26 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0005_category_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.BigIntegerField(verbose_name='Количество'),
        ),
    ]
