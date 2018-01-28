from django.db import models
from django.utils import timezone

class AlgorithmLogs(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    worker_name = models.CharField(max_length=32)

    algorithm_id = models.IntegerField()
    algorithm_name = models.CharField(max_length=16)
    active_time = models.IntegerField()
    server = models.CharField(max_length=8)
    rate = models.FloatField()
    rate_unit = models.CharField(max_length=8)

class WorkerActivityLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    time_since_last = models.FloatField()
    algorithms = models.ManyToManyField(AlgorithmLogs)

class Worker(models.Model):
    name = models.CharField(max_length=16)
    power_draw = models.FloatField()
    running_cost = models.FloatField()
    purchase_cost = models.FloatField()

    gtx1060 = models.IntegerField()
    gtx1070 = models.IntegerField()
    gtx1070ti = models.IntegerField()
    gtx1080 = models.IntegerField()
    gtx1080ti = models.IntegerField()

    activity_log = models.ManyToManyField(WorkerActivityLog)

class AlgorithmBalanceLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    algorithm_id = models.IntegerField()
    algorithm_name = models.CharField(max_length=16)
    balance = models.FloatField()
    balance_change = models.FloatField()
    time_change = models.FloatField()

class PaymentLog(models.Model):
    timestamp = models.DateTimeField()
    amount = models.FloatField()
    fee = models.FloatField()
    TXID = models.CharField(max_length=64)

class BalanceLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    balance = models.FloatField()
    payments_to_date = models.FloatField()
    fees_to_date = models.FloatField()
    net_earnings = models.FloatField()
    gross_earnings = models.FloatField()
    net_change = models.FloatField()
    time_change = models.FloatField()

    algorithm_balances = models.ManyToManyField(AlgorithmBalanceLog)

