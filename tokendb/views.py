from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from tokendb.models import Token
from tokendb.serializers import TokenSerializer


class TokenViewSet(ViewSet):
    """
    API ViewSet for Token
    """

    permission_classes = (IsAuthenticated, IsAdminUser)

    def list(self, request):
        tokens = TokenSerializer(
            Token.objects.all().order_by('-id'), many=True)
        return Response(tokens.data)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            token = Token.objects.get(id=pk)
            serializer = TokenSerializer(
                token, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
