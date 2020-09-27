from django.utils.timezone import now

from rest_framework import serializers

from tokendb.serializers import TokenSerializer

from votingsessions.utils import get_current_session, get_next_session
from votingsessions.models import VotingSession


class VotingSessionSerializer(serializers.ModelSerializer):
    tokens = TokenSerializer(read_only=True, many=True)

    def validate(self, values):
        if self.instance:
            if self.instance.end_date < now().date():
                raise serializers.ValidationError(
                    'Past session can\'t be edited')
            if 'start_date' in values:
                if self.instance.start_date < now().date() and\
                        self.instance.end_date > now().date():
                    raise serializers.ValidationError(
                        'Current session\'s start date can\'t be edited once' +
                        ' started')
            if 'end_date' in values:
                if self.instance == get_current_session() and \
                        values['end_date'] >= get_next_session().start_date:
                    raise serializers.ValidationError(
                        'Current session\'s end date can\'t be greater than' +
                        ' or equal to next sessions start date')
        return values

    class Meta:
        model = VotingSession
        fields = '__all__'
