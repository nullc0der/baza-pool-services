from django.contrib.auth import login

from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from knox.views import LoginView as KnoxLoginView

# TODO: Test endpoints from normal user token


class LoginView(GenericAPIView, KnoxLoginView):
    """
    This view will be used to log in an user
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_staff:
            login(request, user)
            response = super(LoginView, self).post(request, format=None)
            response.data['username'] = user.username
            return response
        return Response(
            {'non_field_errors': ['You don\'t have access to this site']},
            status=status.HTTP_403_FORBIDDEN)
