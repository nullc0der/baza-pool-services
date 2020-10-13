from rest_framework import serializers

from votingpayment.utils import get_token_price

from poolstats.models import PoolInfo


class PoolInfoSerializer(serializers.ModelSerializer):
    last_price = serializers.SerializerMethodField()

    def get_last_price(self, obj):
        return get_token_price(obj.symbol)

    class Meta:
        model = PoolInfo
        fields = (
            'id', 'name', 'symbol', 'logo_url', 'pool_url',
            'pool_stats_api_url', 'last_price',
        )
