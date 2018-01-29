from datetime import datetime
from pytz import timezone as tz

from django.utils import timezone

from .models import (
    AlgorithmLog,
    AlgorithmUtilisation,
    WorkerActivityLog,
    PaymentLog,
    BalanceLog,
    AlgorithmBalanceLog
)

from WAW.models import Wallet

from .currencies import getBTCExchangeRate

def createAlgorithmLog(algo, worker, save=True):
    algorithm_log = AlgorithmLog()
    algorithm_log.worker_name = worker

    algorithm_log.algorithm_id = algo['algorithm_id']
    algorithm_log.algorithm_name = algo['algorithm_name']
    algorithm_log.active_time = algo['active_time']
    algorithm_log.difficulty = algo['difficulty']
    algorithm_log.server_id = algo['server_id']
    algorithm_log.server_name = algo['server_name']

    if save:
        algorithm_log.save()

    addToAlgorithmUtilisation(algorithm_log)

    return algorithm_log

def addToAlgorithmUtilisation(algorithm_log):
    try:
        algorithm_utilisation = AlgorithmUtilisation.objects.get(algorithm_id=algorithm_log.algorithm_id)
        algorithm_utilisation.count += 1
    except AlgorithmUtilisation.DoesNotExist:
        algorithm_utilisation = AlgorithmUtilisation()
        algorithm_utilisation.algorithm_id = algorithm_log.algorithm_id
        algorithm_utilisation.algorithm_name = algorithm_log.algorithm_name
        algorithm_utilisation.count = 1

    algorithm_utilisation.save()
    return algorithm_utilisation

def backdateAlgorithmUtilisation():
    for log in AlgorithmLog.objects.all():
        createAlgorithmLog({
            'algorithm_id': log.algorithm_id,
            'algorithm_name': log.algorithm_name,
            'active_time': log.active_time,
            'difficulty': log.difficulty,
            'server_id': log.server_id,
            'server_name': log.server_name
        }, '', save=False)

def printAlgorithmLogInfo(algorithm_log, addr):
    print('%s:\t****%s: %s is mining %s on the %s server and has been for %s minutes.' % (
        timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        addr[29:],
        algorithm_log.worker_name,
        algorithm_log.algorithm_name,
        algorithm_log.server_name,
        algorithm_log.active_time
    ))

def createWorkerActivityLog(worker_model):
    worker_activity_log = WorkerActivityLog()
    worker_activity_log.worker_name = worker_model.name

    try:
        last_log = worker_model.activity_log.all().order_by('-timestamp')[0]
        worker_activity_log.time_since_last = (timezone.now() - last_log.timestamp).total_seconds()
    except IndexError:
        worker_activity_log.time_since_last = None

    worker_activity_log.save()
    return worker_activity_log

def createPaymentLog(payment, safe_address):
    payment_model = PaymentLog()
    payment_model.wallet_address = safe_address
    payment_model.amount = payment['amount']
    payment_model.fee = payment['fee']
    payment_model.TXID = payment['TXID']
    payment_model.timestamp = datetime.strptime(payment['time'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz('UTC'))
    payment_model.save()

def createBalanceLog(balance, wallet_model, exchange_rate):
    balance_model = BalanceLog()
    balance_model.wallet_address = wallet_model.hidden_address()

    balance_model.GBP_per_BTC = exchange_rate
    balance_model.balance = balance

    payments_to_date = 0
    fees_to_date = 0

    for payment in wallet_model.payment_history.all():
        payments_to_date += payment.amount
        fees_to_date += payment.fee

    balance_model.payments_to_date = payments_to_date
    balance_model.fees_to_date = fees_to_date
    balance_model.net_earnings = balance_model.balance + balance_model.payments_to_date + balance_model.fees_to_date
    balance_model.gross_earnings = balance_model.balance + balance_model.payments_to_date

    try:
        last_balance_model = wallet_model.balance_history.all().order_by('-timestamp')[0]
        dt = (timezone.now() - last_balance_model.timestamp).total_seconds()
        dB = balance_model.net_earnings - last_balance_model.net_earnings
        dBdt = dB / (dt / (60 * 60 * 24))
        balance_model.net_change = dB
        balance_model.time_change = dt
        balance_model.earning_rate = dBdt
    except:
        balance_model.net_change = None
        balance_model.time_change = None
        balance_model.earning_rate = None
        balance_model.earning_rate_GBP = None

    balance_model.save()
    return balance_model

def printBalanceLogInfo(balance_model):
    print('%s:\t%s => Balance: %.8fBTC (£%.2f)\tRate: %.8fBTC/day (£%.2f/day)' % (
        timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        balance_model.wallet_address,
        balance_model.balance,
        balance_model.inGBP('balance'),
        balance_model.earning_rate or 0,
        balance_model.inGBP('earning_rate') or 0
    ))

def updateWalletModel(wallet_model, balance_model):
    wallet_model.balance = balance_model.balance
    wallet_model.payments_to_date = balance_model.payments_to_date
    wallet_model.fees_to_date = balance_model.fees_to_date
    wallet_model.net_earnings = balance_model.net_earnings
    wallet_model.gross_earnings = balance_model.gross_earnings
    wallet_model.net_change = balance_model.net_change
    wallet_model.cumulative_net_GBP += balance_model.inGBP('net_change')
    wallet_model.time_change = balance_model.time_change
    wallet_model.earning_rate = balance_model.earning_rate
    wallet_model.GBP_per_BTC = balance_model.GBP_per_BTC
    wallet_model.balance_history.add(balance_model)
    wallet_model.save()

    return wallet_model

def createAlgorithmBalanceLog(algo, safe_address):
    algo_balance_model = AlgorithmBalanceLog()
    algo_balance_model.wallet_address = safe_address
    algo_balance_model.algorithm_id = algo['algorithm_id']
    algo_balance_model.algorithm_name = algo['algorithm_name']
    algo_balance_model.balance = algo['balance']
    algo_balance_model.save()

    return algo_balance_model

def backdateBTCBalanceLogs():
    exchange_rate = getBTCExchangeRate('BTC', 'GBP')

    for wallet in Wallet.objects.all():
        wallet.cumulative_net_GBP = 0
        index = 0

        for balance_log in wallet.balance_history.all().order_by('-timestamp'):
            if not balance_log.GBP_per_BTC:
                balance_log.GBP_per_BTC = exchange_rate
                balance_log.save()
            if not wallet.GBP_per_BTC:
                wallet.GBP_per_BTC = exchange_rate
            if index == 0:
                wallet.cumulative_net_GBP += balance_log.inGBP('net_earnings')
            else:
                wallet.cumulative_net_GBP += balance_log.inGBP('net_change')
            wallet.save()
            index += 1