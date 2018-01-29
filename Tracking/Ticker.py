from time import sleep

from Tracking.NiceHashClient import NiceHashClient
from Tracking.models import PaymentLog
from Tracking.utils import (
    createAlgorithmLog,
    createWorkerActivityLog,
    printAlgorithmLogInfo,
    createPaymentLog,
    createBalanceLog,
    updateWalletModel,
    createAlgorithmBalanceLog,
    printBalanceLogInfo
)
from .currencies import getBTCExchangeRate
from WAW.models import Wallet, Worker

def wallet_dict():
    wallets = Wallet.objects.all()
    clients = {}

    for wallet in wallets:
        clients[wallet.address] = NiceHashClient(wallet.address, None)

    return clients

def trackActivity(interval: int=600):
    clients = wallet_dict()
    dont_break = True
    while dont_break:
        for address in clients:
            saveActivityData(clients[address])

        print()
        sleep(interval)

def trackBalance(interval: int=600):
    clients = wallet_dict()
    exchange_rate = getBTCExchangeRate('BTC', 'GBP')
    dont_break = True
    while dont_break:
        for address in clients:
            saveBalanceData(clients[address], exchange_rate)

        print()
        sleep(interval)

def saveActivityData(client):
    data = client.get.ActivityData()

    if data and not 'cached_data' in data:
        for worker in data:
            worker_model = Worker.objects.get(name=worker)
            worker_activity_log = createWorkerActivityLog(worker_model)

            for algo in data[worker]:
                algorithm_log = createAlgorithmLog(algo, worker)
                worker_activity_log.algorithms.add(algorithm_log)
                printAlgorithmLogInfo(algorithm_log, client.addr)

            worker_activity_log.save()
            worker_model.activity_log.add(worker_activity_log)
            worker_model.save()

def saveBalanceData(client, exchange_rate):
    data = client.get.BalanceData()

    if data and not 'cached_data' in data:
        wallet_model = Wallet.objects.get(address=client.addr)
        safe_address = wallet_model.hidden_address()

        for payment in data['payments']:
            payment_model = PaymentLog.objects.filter(TXID=payment['TXID'])
            if not len(payment_model):
                payment_model = createPaymentLog(payment, safe_address)
                wallet_model.payment_history.add(payment_model)
                wallet_model.save()

        balance_model = createBalanceLog(data['balance'], wallet_model, exchange_rate)
        updateWalletModel(wallet_model, balance_model)

        for algo in data['algo_balances']:
            algo_balance_model = createAlgorithmBalanceLog(algo, safe_address)
            balance_model.algorithm_balances.add(algo_balance_model)

        balance_model.save()

        printBalanceLogInfo(balance_model)