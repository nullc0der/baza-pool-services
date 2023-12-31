from rest_framework import serializers

from tokendb.models import Token

from votingpayment.models import VotingPayment


class VotingPaymentSerializer(serializers.ModelSerializer):
    token_id = serializers.IntegerField(write_only=True)
    amount = serializers.FloatField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    def validate_tx_hash(self, value):
        try:
            VotingPayment.objects.get(tx_hash=value)
            raise serializers.ValidationError(
                'Transaction hash was submitted before')
        except VotingPayment.DoesNotExist:
            return value

    def validate_token_id(self, value):
        try:
            Token.objects.get(id=value)
            return value
        except Token.DoesNotExist:
            raise serializers.ValidationError('No token exists')

    class Meta:
        model = VotingPayment
        fields = ('id', 'amount', 'timestamp', 'tx_hash', 'token_id', )
