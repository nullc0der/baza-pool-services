from operator import itemgetter

from tokendb.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from votingsessions.models import VotingSession
from votingsessions.serializers import VotingSessionSerializer
from votingsessions.utils import get_current_session, get_next_session


class VotingSessionViewSet(ViewSet):
    """
    API ViewSet for VotingSession admin
    """

    permission_classes = (IsAuthenticated, IsAdminUser, )

    def list(self, request):
        current_session = VotingSessionSerializer(get_current_session()).data
        next_session = VotingSessionSerializer(get_next_session()).data
        past_sessions = VotingSessionSerializer(
            VotingSession.objects.all().exclude(
                id__in=[current_session['id'],
                        next_session['id']]).order_by('-id'),
            many=True).data
        current_session['tokens'] = sorted(
            current_session['tokens'], key=itemgetter('amount_raised'),
            reverse=True)
        data = {
            'current_session': current_session,
            'next_session': next_session,
            'past_sessions': past_sessions
        }
        return Response(data)

    def partial_update(self, request, pk=None):
        try:
            voting_session = VotingSession.objects.get(id=pk)
            serializer = VotingSessionSerializer(
                voting_session, context={'voting_session': voting_session},
                data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except VotingSession.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ToggleTokenVisibilityInSession(APIView):
    """
    This view will be used to toggle a tokens visibility in
    a session
    """

    permission_classes = (IsAuthenticated, IsAdminUser, )

    def post(self, request, session_id, token_id):
        try:
            visible = False
            session = VotingSession.objects.get(id=session_id)
            token = Token.objects.get(id=token_id)
            hidden_tokens_id = session.get_hidden_tokens_id()
            if str(token.id) in hidden_tokens_id:
                hidden_tokens_id.remove(str(token.id))
                visible = True
            else:
                hidden_tokens_id.append(str(token.id))
            session.hidden_tokens_id = ','.join(hidden_tokens_id)
            session.save()
            return Response(
                {
                    'visible': visible,
                    'token_id': token.id,
                    'session_id': session.id
                }
            )
        except (VotingSession.DoesNotExist, Token.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)


class CurrentVotingSessionView(APIView):
    """
    This view will be used to get current session in landing
    """

    def get(self, request, format=None):
        current_session = VotingSessionSerializer(get_current_session()).data
        current_session['tokens'] = [
            token for token in current_session['tokens']
            if str(token['id']) not in current_session['hidden_tokens_id']]
        current_session['tokens'] = sorted(
            current_session['tokens'], key=itemgetter('amount_raised'),
            reverse=True)
        del current_session['hidden_tokens_id']
        return Response(current_session)
