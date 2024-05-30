from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, GetUserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def test(request):
    #For application/json
    print("Hello:   ", request.data)
    #For application/form
    # print("Hello:   " + request.POST)
    return Response({"msg": "Your test is success!", "post": request.POST, "data": request.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def checkToken(request):
    return Response({"valid": true}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"msg": "Invalid Password!"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(instance=user)
    try:
        token = Token.objects.get(user=user)
        if not token.is_expired():
            return Response({"msg": "You are already logged in!"}, status=status.HTTP_200_OK)
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
    #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"msg": "Invalid register data!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = get_object_or_404(User, username=request.data['username'])
    serializer = GetUserSerializer(instance=user)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    token = Token.objects.get(user=request.user)
    if token:
        token.delete()
        return Response({"msg": "You have been successfully logged out"}, status.HTTP_200_OK)
    return Response({"msg": "You not logged!"}, status=status.HTTP_400_BAD_REQUEST)
