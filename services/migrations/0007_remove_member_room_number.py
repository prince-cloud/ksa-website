# Generated by Django 3.1.4 on 2022-04-02 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20220402_0247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='room_number',
        ),
    ]
