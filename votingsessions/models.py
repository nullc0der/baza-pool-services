from django.db import models

from tokendb.models import Token

# Create your models here.


class VotingSession(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    minimum_amount_per_token = models.PositiveIntegerField()
    description = models.TextField()
    is_paused = models.BooleanField(default=False)
    tokens = models.ManyToManyField(Token)
