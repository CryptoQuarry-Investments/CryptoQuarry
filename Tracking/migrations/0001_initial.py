# Generated by Django 2.0 on 2018-01-28 20:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlgorithmBalanceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('algorithm_id', models.IntegerField()),
                ('algorithm_name', models.CharField(max_length=16)),
                ('balance', models.FloatField()),
                ('balance_change', models.FloatField()),
                ('time_change', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AlgorithmLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('worker_name', models.CharField(max_length=32)),
                ('algorithm_id', models.IntegerField()),
                ('algorithm_name', models.CharField(max_length=16)),
                ('active_time', models.IntegerField()),
                ('server_name', models.CharField(max_length=8)),
                ('server_id', models.IntegerField()),
                ('difficulty', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='BalanceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('balance', models.FloatField()),
                ('payments_to_date', models.FloatField()),
                ('fees_to_date', models.FloatField()),
                ('net_earnings', models.FloatField()),
                ('gross_earnings', models.FloatField()),
                ('net_change', models.FloatField()),
                ('time_change', models.FloatField()),
                ('algorithm_balances', models.ManyToManyField(to='Tracking.AlgorithmBalanceLog')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('amount', models.FloatField()),
                ('fee', models.FloatField()),
                ('TXID', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='WorkerActivityLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_since_last', models.FloatField(null=True)),
                ('algorithms', models.ManyToManyField(to='Tracking.AlgorithmLog')),
            ],
        ),
    ]