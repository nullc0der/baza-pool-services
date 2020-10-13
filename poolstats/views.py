from rest_framework.response import Response
from rest_framework.views import APIView

from poolstats.serializers import PoolInfoSerializer
from poolstats.models import PoolInfo


class OwnedPoolsInfoView(APIView):
    """
    This view will send owned pool info
    """

    def get(self, request, format=None):
        poolinfo_data = PoolInfoSerializer(
            PoolInfo.objects.all(), many=True).data
        return Response(poolinfo_data)
