# Generated by Django 4.2.1 on 2023-05-25 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweetLand', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]