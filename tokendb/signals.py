from django.db.models.signals import post_save
from django.dispatch import receiver

from tokendb.models import Token

from votingsessions.utils import get_current_session, get_next_session


@receiver(post_save, sender=Token)
def add_token_to_voting_sessions(sender, **kwargs):
    current_session = get_current_session()
    next_session = get_next_session()
    current_session.tokens.add(kwargs['instance'])
    next_session.tokens.add(kwargs['instance'])
