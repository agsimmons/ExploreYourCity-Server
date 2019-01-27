from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.permissions
from . import serializers


class UserRegister(APIView):
    permission_classes = (rest_framework.permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # TODO: Deactivate user account and send verification email which re-activates account
            # user.is_active = False
            # user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
