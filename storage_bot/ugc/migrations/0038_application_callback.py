# Generated by Django 3.2.7 on 2021-11-16 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0037_alter_profile_selected_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application_callback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appl', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.applications')),
            ],
        ),
    ]