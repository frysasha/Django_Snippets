# Generated by Django 3.1 on 2022-05-26 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_auto_20220525_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
