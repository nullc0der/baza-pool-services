from django.utils.timezone import now, timedelta

from votingsessions.models import VotingSession


def get_current_session():
    voting_sessions = VotingSession.objects.filter(
        start_date__lte=now(), end_date__gt=now())
    if not voting_sessions:
        next_sessions = VotingSession.objects.filter(
            start_date__gt=now()
        )
        current_session = next_sessions[0]
        current_session.start_date = now().date()
        current_session.save()
        return current_session
    return voting_sessions[0]


def get_next_session():
    current_session = get_current_session()
    next_sessions = VotingSession.objects.filter(
        start_date__gt=current_session.end_date)
    if not next_sessions:
        next_session = VotingSession.objects.create(
            start_date=current_session.end_date + timedelta(days=1),
            end_date=current_session.end_date + timedelta(days=31),
            minimum_amount_per_token=4000
        )
        return next_session
    return next_sessions[0]
