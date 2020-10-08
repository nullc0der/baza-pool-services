from rest_framework import serializers

from tokendb.models import Token


# TODO: Add total_vote, baza_earned
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
