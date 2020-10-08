from django.utils.timezone import datetime

from votingpayment.api_wrapper import ApiWrapper
from votingpayment.models import VotingPayment


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
