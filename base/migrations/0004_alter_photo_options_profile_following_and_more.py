# Generated by Django 4.1.4 on 2023-06-18 04:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_post_upload_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'verbose_name': 'Photo'},
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='followers', to='base.profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='upload_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2023, 6, 18, 4, 26, 4, 367909, tzinfo=datetime.timezone.utc)),
        ),
    ]
