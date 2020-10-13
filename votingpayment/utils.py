import requests

from django.utils.timezone import datetime, timedelta, now
from django.core.cache import cache

from votingpayment.api_wrapper import ApiWrapper
from votingpayment.models import VotingPayment


def get_token_price(token_symbol: str) -> float:
    fetch_data = False
    token_prices = cache.get('token_prices')
    token_price = token_prices.get(token_symbol, {})
    if token_price:
        if token_price['last_fetched'] + timedelta(hours=1) < now():
            fetch_data = True
    else:
        fetch_data = True
    if fetch_data:
        res = requests.get(
            'https://www.southxchange.com/api/price/{}/TUSD'.format(
                token_symbol))
        if res.status_code == 200:
            token_price['data'] = res.json()
            token_price['last_fetched'] = now()
            token_prices[token_symbol] = token_price
            cache.set('token_prices', token_prices, None)
    return token_price['data']['Last']


def check_pending_payments() -> None:
    apiwrapper = ApiWrapper()
    res = apiwrapper.get_wallet_transactions()
    if res.status_code == 200:
        transactions = res.json()['transactions']
        for transaction in transactions:
            try:
                votingpayment = VotingPayment.objects.get(
                    tx_hash=transaction['hash'])
                votingpayment.amount = transaction['transfers'][0]['amount']
                votingpayment.timestamp = datetime.fromtimestamp(
                    transaction['timestamp'])
                votingpayment.save()
            except VotingPayment.DoesNotExist:
                pass
