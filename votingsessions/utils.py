from django.utils.timezone import now

from votingsessions.models import VotingSession


def get_current_session():
    voting_sessions = VotingSession.objects.filter(
        start_date__lte=now(), end_date__gt=now())
    return voting_sessions[0]


def get_next_session():
    current_session = get_current_session()
    next_sessions = VotingSession.objects.filter(
        start_date__gt=current_session.end_date)
    return next_sessions[0]
