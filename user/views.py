from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication
from user.models import User, Token
from.serializers import UserSerializer, RegUserSerializer, SuUserSerializer


@api_view(['POST'])
def CheckToken(request):
    return Response({"detail": "Your token is valid"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    if request.data.get('email'):
        user = get_object_or_404(User, email=request.data['email'])
    elif request.data.get('username'):
        user = get_object_or_404(User, username=request.data['username'])
    else:
        return Response({"detail": "Field Username or Email required!"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(request.data['password']):
        return Response({"msg": "Invalid Password!"}, status=status.HTTP_400_BAD_REQUEST)
    # serializer = UserSerializer(instance=user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def Register(request):
    serializer = RegUserSerializer(data=request.data)
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

class ProfilesView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        if request.user.is_admin:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            user = request.auth.token.user
            serializer = UserSerializer(user)
            return Response({"data": serializer.data})

class ProfileView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, id):
        if request.user.is_admin:
            user = get_object_or_404(User, pk=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            if id == request.auth.token.user.id:
                user = get_object_or_404(User, pk=id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return Response({"error": "No tienes permiso para ver esta información"}, status=status.HTTP_403_FORBIDDEN)
    
    def put(self, request, id):
        if request.user.is_admin:
            user = get_object_or_404(User, pk=id)
            if request.user.is_superuser:
                serializer = SuUserSerializer(user, data=request.data, partial=True)
            else:
                serializer = RegUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if id == request.auth.token.user.id:
                user = get_object_or_404(User, pk=id)
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Unauthorized, Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, id):
        if not request.user.is_admin:
            return Response({"detail": "Unauthorized, Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=id)
        if user.id != request.user.id:
            if not user.is_admin or user.is_admin and request.user.is_superuser:
                user.delete()
                return Response({"detail": "User deleted successfully"}, status=status.HTTP_200_OK)
            return Response({"detail": "Only superusers can delete users type adminers"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "You not delete your actual user"},status=status.HTTP_400_BAD_REQUEST)


 