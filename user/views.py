from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication
from user.models import User, Token
from.serializers import UserSerializer


@api_view(['POST'])
def CheckToken(request):
    return Response({"detail": "Your token is valid"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    #if not request.data.get('username'):
    #    return Response({"detail": "Field Username or Email required!"}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"msg": "Invalid Password!"}, status=status.HTTP_400_BAD_REQUEST)
    # serializer = UserSerializer(instance=user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def Register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Logout(request):
    # token = Token.objects.get(user=request.user)
    token = request.auth
    if token:
        token.delete()
        return Response({"msg": "You have been successfully logged out"}, status.HTTP_200_OK)
    return Response({"msg": "You not logged!"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def get(self, request, id):
        if id != request.auth.token.user.id:
            return Response({"detail": "Unauthorized, Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        if id != request.auth.token.user.id:
            return Response({"detail": "Unauthorized, Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        if id != request.auth.token.user.id:
            return Response({"detail": "Unauthorized, Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=id)
        user.delete()
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_200_OK)
