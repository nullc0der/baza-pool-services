from django.utils.timezone import now

from rest_framework import serializers

from tokendb.models import Token

from votingpayment.models import VotingPayment

from votingsessions.utils import get_current_session, get_next_session
from votingsessions.models import VotingSession


class SessionTokenSerializer(serializers.ModelSerializer):
    total_votes = serializers.SerializerMethodField()

    def get_total_votes(self, obj):
        return VotingPayment.objects.filter(
            token=obj, voting_session=self.context['voting_session']).exclude(
            amount__isnull=True, timestamp__isnull=True).count()

    class Meta:
        model = Token
        fields = (
            'id', 'name', 'symbol', 'logo', 'homepage_url',
            'algo', 'is_archived', 'has_won', 'added_date', 'won_date',
            'total_votes'
        )


class VotingSessionSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()
    hidden_tokens_id = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        return SessionTokenSerializer(
            obj.tokens.all().order_by('-id'),
            many=True, context={'voting_session': obj}).data

    def get_hidden_tokens_id(self, obj):
        return obj.get_hidden_tokens_id()

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
