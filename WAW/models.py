from datetime import timedelta

from django.db import models
from django.utils import timezone

from Tracking.models import (
    WorkerActivityLog,
    PaymentLog,
    BalanceLog
)

class Worker(models.Model):
    name = models.CharField(max_length=16)
    power_draw = models.FloatField(default=0)
    running_cost = models.FloatField(default=0)
    purchase_cost = models.FloatField(default=0)

    gtx1060 = models.IntegerField(default=0)
    gtx1070 = models.IntegerField(default=0)
    gtx1070ti = models.IntegerField(default=0)
    gtx1080 = models.IntegerField(default=0)
    gtx1080ti = models.IntegerField(default=0)

    activity_log = models.ManyToManyField(WorkerActivityLog, blank=True)

    def __str__(self):
        return self.name

    def recent_activity(self, output: str='str'):
        try:
            latest_log = self.activity_log.all().order_by('-timestamp')[0]

            if output == 'list':
                out = []

                for algo in latest_log.algorithms.all():
                    out.append({
                        'algorithm_name': algo.algorithm_name,
                        'active_time': algo.active_time
                    })
            else:
                out = ''

                for algo in latest_log.algorithms.all():
                    out += '%s (%s), ' % (algo.algorithm_name, algo.active_time)


            return out
        except IndexError:
            return 'No logs yet'

class Wallet(models.Model):
    address = models.CharField(max_length=48)
    workers = models.ManyToManyField(Worker, blank=True)
    balance = models.FloatField(default=0)
    payments_to_date = models.FloatField(default=0)
    fees_to_date = models.FloatField(default=0)
    net_earnings = models.FloatField(default=0)
    cumulative_net_GBP = models.FloatField(default=0)
    gross_earnings = models.FloatField(default=0)
    net_change = models.FloatField(null=True)
    time_change = models.FloatField(null=True)
    earning_rate = models.FloatField(null=True)
    GBP_per_BTC = models.FloatField(default=0)

    payment_history = models.ManyToManyField(PaymentLog, blank=True)
    balance_history = models.ManyToManyField(BalanceLog, blank=True)

    def __str__(self):
        return self.hidden_address()

    def hidden_address(self):
        return '****%s' % self.address[29:]

    def inGBP(self, property):
        try:
            return getattr(self, property) * self.GBP_per_BTC
        except:
            return False

    def averaged_earning_rate(self, days: float=1, offset: float=0):
        end = timezone.now() - timedelta(days=offset)
        start = end - timedelta(days=days)
        logs = self.balance_history.all().filter(
            timestamp__gte=start,
            timestamp__lte=end
        ).order_by('-timestamp')

        total_GBP = 0

        for log in logs:
            total_GBP += (log.net_change or 0) * log.GBP_per_BTC

        total_BTC = logs.first().net_earnings - logs.last().net_earnings
        total_time = ((logs.first().timestamp - logs.last().timestamp).total_seconds()) / (60 * 60 * 24)

        return {
            'BTC': total_BTC / total_time,
            'GBP': {
                'current': (total_BTC / total_time) * self.GBP_per_BTC,
                'tracked': total_GBP / total_time,
                'max': max([
                    (total_BTC / total_time) * self.GBP_per_BTC,
                    total_GBP / total_time
                ])
            }
        }