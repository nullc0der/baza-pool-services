from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from votingsessions.models import VotingSession
from votingsessions.serializers import VotingSessionSerializer
from votingsessions.utils import get_current_session, get_next_session


class VotingSessionViewSet(ViewSet):
    """
    API ViewSet for VotingSession
    """

    permission_classes = (IsAuthenticated, IsAdminUser, )

    def list(self, request):
        current_session = VotingSessionSerializer(get_current_session()).data
        next_session = VotingSessionSerializer(get_next_session()).data
        past_sessions = VotingSessionSerializer(
            VotingSession.objects.all().exclude(
                id__in=[current_session['id'], next_session['id']]), many=True).data
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
