# Generated by Django 2.0 on 2018-01-28 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracking', '0002_auto_20180128_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='workeractivitylog',
            name='worker_name',
            field=models.CharField(default='Agnew', max_length=32),
        ),
    ]
