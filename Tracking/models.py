from django.db import models
from django.utils import timezone

## ACTIVITY LOGS

class AlgorithmLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    worker_name = models.CharField(max_length=32)

    algorithm_id = models.IntegerField()
    algorithm_name = models.CharField(max_length=16)
    active_time = models.IntegerField()
    server_name = models.CharField(max_length=8)
    server_id = models.IntegerField()
    difficulty = models.FloatField()

    def __str__(self):
        return '%s: %s @ %s' % (
            self.worker_name,
            self.algorithm_name,
            self.timestamp.strftime('%y-%m-%d %H:%M:%S')
        )

class AlgorithmUtilisation(models.Model):
    algorithm_id = models.IntegerField()
    algorithm_name = models.CharField(max_length=32)
    count = models.IntegerField(default=0)

class WorkerActivityLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    time_since_last = models.FloatField(null=True)
    algorithms = models.ManyToManyField(AlgorithmLog, blank=True)
    worker_name = models.CharField(max_length=32)

    def __str__(self):
        return '%s @ %s' % (self.worker_name, self.timestamp.strftime('%y-%m-%d %H:%M:%S'))

## BALANCE LOGS

class AlgorithmBalanceLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    wallet_address = models.CharField(max_length=8)

    algorithm_id = models.IntegerField()
    algorithm_name = models.CharField(max_length=16)
    balance = models.FloatField()

    def __str__(self):
        return '%s: %s @ %s' % (
            self.wallet_address,
            self.algorithm_name,
            self.timestamp.strftime('%y-%m-%d %H:%M:%S')
        )

class PaymentLog(models.Model):
    timestamp = models.DateTimeField()
    wallet_address = models.CharField(max_length=8)

    amount = models.FloatField()
    fee = models.FloatField()
    TXID = models.CharField(max_length=64)

    def __str__(self):
        return '%s: %s' % (self.wallet_address, self.TXID)

class BalanceLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    wallet_address = models.CharField(max_length=8)

    balance = models.FloatField(default=0)
    payments_to_date = models.FloatField(default=0)
    fees_to_date = models.FloatField(default=0)
    net_earnings = models.FloatField(default=0)
    gross_earnings = models.FloatField(default=0)
    net_change = models.FloatField(null=True)
    time_change = models.FloatField(null=True)
    earning_rate = models.FloatField(null=True)
    GBP_per_BTC = models.FloatField(default=0)

    algorithm_balances = models.ManyToManyField(AlgorithmBalanceLog)

    def __str__(self):
        return '%s @ %s' % (
            self.wallet_address,
            self.timestamp.strftime('%y-%m-%d %H:%M:%S')
        )

    def inGBP(self, property):
        try:
            return getattr(self, property) * self.GBP_per_BTC
        except:
            return False