# Generated by Django 4.0.1 on 2022-01-31 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel_info', '0003_rename_about_channelinfo_json_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channelinfo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]