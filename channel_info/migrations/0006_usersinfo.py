# Generated by Django 4.0.1 on 2022-02-01 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel_info', '0005_alter_channelinfo_json'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json', models.JSONField()),
            ],
        ),
    ]
