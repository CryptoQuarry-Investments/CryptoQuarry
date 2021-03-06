from rest_framework import serializers

from .models import Worker, Wallet

class WorkerSerializer(serializers.HyperlinkedModelSerializer):
    recent_activity = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = (
            'name',
            'recent_activity'
        )

    def get_recent_activity(self, object):
        return object.recent_activity(output='list')


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    workers = WorkerSerializer(many=True)
    latest_reading = serializers.SerializerMethodField()
    current_net_GBP = serializers.SerializerMethodField()
    earning_rate = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = (
            'workers',
            'hidden_address',
            'GBP_per_BTC',
            'latest_reading',
            'cumulative_net_GBP',
            'net_earnings',
            'current_net_GBP',
            'earning_rate'
        )

    def get_latest_reading(self, object):
        try:
            log = object.balance_history.all().order_by('-timestamp')[0]
            return log.timestamp.strftime('%H:%M:%S %d %b %Y')
        except IndexError:
            return 'No logs yet'

    def get_current_net_GBP(self, object):
        return object.inGBP('net_earnings')

    def get_earning_rate(self, object):
        return {
            'latest': {
                'BTC': object.earning_rate,
                'GBP': object.inGBP('earning_rate')
            },
            '1d': object.averaged_earning_rate(days=1),
            '1m': object.averaged_earning_rate(days=30),
        }
