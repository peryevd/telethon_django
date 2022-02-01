# Generated by Django 4.0.1 on 2022-02-01 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel_info', '0006_usersinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='MessageReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json', models.JSONField()),
            ],
        ),
    ]
