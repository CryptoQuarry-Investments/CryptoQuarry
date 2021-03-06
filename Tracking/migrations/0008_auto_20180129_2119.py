# Generated by Django 2.0 on 2018-01-29 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracking', '0007_algorithmutilisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='balancelog',
            name='GBP_per_BTC',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='balancelog',
            name='balance',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='balancelog',
            name='fees_to_date',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='balancelog',
            name='gross_earnings',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='balancelog',
            name='net_earnings',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='balancelog',
            name='payments_to_date',
            field=models.FloatField(default=0),
        ),
    ]
