from django.shortcuts import render
from rest_framework.authtoken.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.conf import settings
from django.shortcuts import redirect
from custom_auth.serializers import UserSerializer, LoginSerializer
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from .models import User
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Your account has been activated successfully.")
        else:
            return HttpResponse("Activation link is invalid.")
        
class VerifyTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Verify a token sent by the frontend is valid.

        The frontend token is compared with the user's token in the request's
        authentication header. If the two match, a 200 response is returned,
        indicating that the token is valid. If the two do not match, a 401
        response is returned, indicating that the token is not valid.

        :param request: The request object
        :return: A response with a status of 200 if the token is valid, 401 otherwise
        """
        frontend_token = request.data.get('token')
        user_token = request.auth
        
        if frontend_token == str(user_token):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)