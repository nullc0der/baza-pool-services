# TODO: Proper pool info model and API, USDT<->BAZA
from rest_framework.response import Response
from rest_framework.views import APIView


class OwnedPoolsInfoView(APIView):
    """
    This view will send owned pool info
    """

    def get(self, request, format=None):
        return Response([{'name': 'BAZA', }])
