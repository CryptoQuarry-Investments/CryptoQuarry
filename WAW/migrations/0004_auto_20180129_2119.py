# Generated by Django 2.0 on 2018-01-29 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WAW', '0003_auto_20180128_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='GBP_per_BTC',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='wallet',
            name='cumulative_net_GBP',
            field=models.FloatField(default=0),
        ),
    ]