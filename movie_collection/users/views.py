from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer




class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token),
                "redirect": "http://localhost:3000"
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                refresh_token = RefreshToken.for_user(user)
                return Response({
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh_token),
                    "access": str(refresh_token.access_token),
                    "redirect": "http://localhost:3000"
                },status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
            
    permission_classes = [IsAuthenticated]
    def post(self, request, user_name):
        try:
            user_to_unfollow = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            follow = Follow.objects.get(follower=request.user, followed=user_to_unfollow)
            follow.delete()
            return Response({'message': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({'message': f'You are not following {user_to_unfollow.username}'}, status=status.HTTP_400_BAD_REQUEST)