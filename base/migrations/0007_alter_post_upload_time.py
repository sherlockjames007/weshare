# Generated by Django 4.1.4 on 2023-06-18 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_post_upload_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
