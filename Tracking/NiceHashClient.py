import json
import math
import requests
from Backend.SimpleCache import Cache

algo_map = [
    'Scrypt',
    'SHA256',
    'ScryptNf',
    'X11',
    'X13',
    'Keccak',
    'X15',
    'Nist5',
    'NeoScrypt',
    'Lyra2RE',
    'WhirlpoolX',
    'Qubit',
    'Quark',
    'Axiom',
    'Lyra2REv2',
    'ScryptJaneNf16',
    'Blake256r8',
    'Blake256r14',
    'Blake256r8vnl',
    'Hodl',
    'DaggerHashimoto',
    'Decred',
    'CryptoNight',
    'Lbry',
    'Equihash',
    'Pascal',
    'X11Gost',
    'Sia',
    'Blake2s',
    'Skunk',
]
server_map = [
    'EU',
    'US',
    'HK',
    'JP'
]
default_methods = {
    'activity': 'stats.provider.workers',
    'balance': 'stats.provider'
}

class NiceHashClient:
    def __init__(
        self,
        addr: str,
        methods: dict,
        endpoint: str='https://api.nicehash.com/api',
    ):
        self.addr = addr
        self.methods = methods or default_methods
        self.endpoint = endpoint
        self.cache = Cache()
        self.get = _NiceHashGetRequests(
            addr=self.addr,
            methods=self.methods,
            endpoint=self.endpoint,
            cache=self.cache
        )



class _NiceHashGetRequests:
    def __init__(
        self,
        addr: str,
        methods: dict,
        endpoint: str='https://api.nicehash.com/api',
        cache=None,
    ):
        self.addr = addr
        self.methods = methods
        self.endpoint = endpoint
        self.cache = cache
        self.formatter = _NiceHashGetResponseFormatter(
            cache=self.cache,
        )

    @staticmethod
    def AlgorithmMap(expiry=0):
        return algo_map

    @staticmethod
    def ServerMap(expiry=0):
        return server_map

    def ActivityData(self, expiry=300):
        # Check cache for data
        cached_data = False
        if self.cache and expiry > 0:
            cached_data = self.cache.get('activity_data', expiry)

        if cached_data and not cached_data['expired']:
            return cached_data
        else:
            try:
                req = requests.get(
                    self.endpoint,
                    params={'method': self.methods['activity'], 'addr': self.addr}
                )

                data = self.formatter.ActivityData(req.json())

                if self.cache:
                    self.cache.set('activity_data', data)

                return data
            except json.decoder.JSONDecodeError:
                return cached_data

    def BalanceData(self, expiry=300):
        # Check cache for data
        cached_data = False
        if self.cache and expiry > 0:
            cached_data = self.cache.get('balance_data', expiry)

        if cached_data and not cached_data['expired']:
            return cached_data
        else:
            try:
                req = requests.get(
                    self.endpoint,
                    params={'method': self.methods['balance'], 'addr': self.addr}
                )

                data = self.formatter.BalanceData(req.json())

                if self.cache:
                    self.cache.set('balance_data', data)

                return data
            except json.decoder.JSONDecodeError:
                return cached_data

class _NiceHashGetResponseFormatter:
    def __init__(
        self,
        cache=None
    ):
        self.cache = cache

    def ActivityData(self, response):
        seen_names = []
        formatted_data = {}

        for worker in response['result']['workers']:
            seen_names.append(worker[0])

            try:
                server = _NiceHashGetRequests.ServerMap()[worker[5]]
            except IndexError:
                server = worker[5]
            except KeyError:
                server = worker[5]

            try:
                algo = _NiceHashGetRequests.AlgorithmMap()[worker[6]]
            except IndexError:
                algo = worker[6]
            except KeyError:
                algo = worker[6]

            try:
                formatted_data[worker[0]]
            except KeyError:
                formatted_data[worker[0]] = []

            formatted_data[worker[0]].append({
                'name': worker[0] + ':' + str(seen_names.count(worker[0])),
                'machine_name': worker[0],
                'active_time': worker[2],
                'difficulty': worker[4],
                'server_name': server,
                'server_id': worker[5],
                'algorithm_name': algo,
                'algorithm_id': worker[6],
            })

        return formatted_data

    def BalanceData(self, response):
        algo_results = []
        total_balance = 0

        for algo_data in response['result']['stats']:
            try:
                algo = _NiceHashGetRequests.AlgorithmMap()[algo_data['algo']]
            except:
                algo = algo_data['algo']

            if float(algo_data['balance']) > 1e-5:
                total_balance += math.floor(float(algo_data['balance']) * 1e8) / 1e8

            algo_results.append({
                'algorithm_name': algo,
                'algorithm_id': algo_data['algo'],
                'balance': float(algo_data['balance']),
            })

        return {
            'balance': total_balance,
            'algo_balances': algo_results,
            'payments': response['result']['payments']
        }