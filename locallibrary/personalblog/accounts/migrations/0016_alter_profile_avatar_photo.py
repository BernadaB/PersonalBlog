# Generated by Django 3.2.5 on 2021-08-29 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_profile_avatar_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar_photo',
            field=models.ImageField(default='static/main/assets/images/download.jpg', upload_to='profile_photo'),
        ),
    ]