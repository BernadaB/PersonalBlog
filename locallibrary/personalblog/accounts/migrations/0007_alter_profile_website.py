# Generated by Django 3.2 on 2021-05-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]
