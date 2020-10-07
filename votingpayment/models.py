from django.db import models

from tokendb.models import Token
from votingsessions.models import VotingSession

# Create your models here.


class VotingPayment(models.Model):
    token = models.ForeignKey(
        Token, on_delete=models.CASCADE, related_name='voting_payments')
    voting_session = models.ForeignKey(
        VotingSession, on_delete=models.CASCADE,
        related_name='voting_payments')
    amount = models.FloatField(null=True)
    timestamp = models.DateTimeField(null=True)
    tx_hash = models.CharField(max_length=100)
    tx_from_address = models.CharField(max_length=100)
