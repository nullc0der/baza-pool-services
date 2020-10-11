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
    # If multiple, must be seperated by comma(,)
    hidden_tokens_id = models.TextField(default='', max_length=400)

    def get_hidden_tokens_id(self):
        return self.hidden_tokens_id.split(',')
