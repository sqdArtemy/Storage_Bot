# Generated by Django 3.2.7 on 2021-09-25 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('region', models.TextField(verbose_name='Область')),
                ('city', models.TextField(verbose_name='Город')),
                ('adress', models.TextField(verbose_name='Адресс')),
                ('phone', models.BigIntegerField(verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль пользователя', 'verbose_name_plural': 'Профили пользователей'},
        ),
    ]
