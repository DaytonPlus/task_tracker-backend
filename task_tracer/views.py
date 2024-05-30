from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

from crud.models import Token


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(instance=user)
    try:
        token = Token.objects.get(user=user)
        if not token.is_expired():
            return Response({"message": "You are already logged in"}, status=status.HTTP_200_OK)
        else:
            token.delete()
            token = Token.objects.create(user=user)
    except Token.DoesNotExist:
            token = Token.objects.create(user=user)
    return Response({"token": token.key}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    ## In test
    token = request.auth
    if token:
        token.update_expiration_time()
    ## In test

    user = get_object_or_404(User, username=request.data['username'])
    serializer = UserSerializer(instance=user)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    ## In test
    token= request.auth
    if token:
        token.delete()
    request.user.auth_token.delete()
    ## In test

    return Response({"message": "You have been successfully logged out"}, status.HTTP_200_OK)

