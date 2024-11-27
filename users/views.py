from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
# Create your views here.
User = get_user_model()


# 用户注册接口
class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error":"用户名和密码是必填项"},status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error":"用户名已经存在"},status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username,password=password)
        return Response({"message":"注册成功","user_id":user.id},status=status.HTTP_201_CREATED)

# 用户登陆接口
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 添加额外的信息到令牌
        token['username'] = user.username
        return token
    

class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer