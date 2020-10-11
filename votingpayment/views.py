from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from tokendb.models import Token
from votingpayment.models import VotingPayment
from votingsessions.models import VotingSession
from votingsessions.utils import get_current_session
from votingpayment.serializers import VotingPaymentSerializer
from votingpayment.api_wrapper import ApiWrapper

# Create your views here.


class VotingPaymentView(APIView):
    """
    This API will be used for vote for a token
    """

    def post(self, request, format=None):
        serializer = VotingPaymentSerializer(data=request.data)
        if serializer.is_valid():
            voting_session = get_current_session()
            if not voting_session.is_paused:
                token = Token.objects.get(
                    id=serializer.validated_data['token_id'])
                serializer.save(token=token, voting_session=voting_session)
                return Response()
            return Response(
                {'non_field_errors': ['Voting session is paused']},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VotingPaymentAddress(APIView):
    """
    This API will be used to get address of payment wallet
    """

    def get(self, request, format=None):
        if settings.SITE_TYPE != 'local':
            apiwrapper = ApiWrapper()
            res = apiwrapper.get_wallet_address()
            if res.status_code == 200:
                return Response({'wallet_address': res.json()['address']})
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VotingPaymentAdminView(APIView):
    """
    This API will be used to get all votes for a token
    in a particular session
    """

    permission_classes = (IsAuthenticated, IsAdminUser, )

    def get(self, request, session_id, token_id, format=None):
        try:
            voting_session = VotingSession.objects.get(id=session_id)
            token = Token.objects.get(id=token_id)
            voting_payments = VotingPaymentSerializer(
                VotingPayment.objects.filter(
                    token=token, voting_session=voting_session).exclude(
                    amount__isnull=True, timestamp__isnull=True),
                many=True).data
            data = {
                'voting_payments': voting_payments,
                'total': sum(payment['amount'] for payment in voting_payments)
            }
            return Response(data)
        except (VotingSession.DoesNotExist, Token.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
