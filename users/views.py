from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from users.serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            return Response({
                "success": False,
                "code": 20001,
                "message": "用户名或密码错误",
                "data": {},
            })
        
        token = serializer.validated_data.get('access')
        refresh_token = serializer.validated_data.get('refresh')
        
        response_data = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": {
                "token": str(token),
                # "refresh_token": str(refresh_token),
            }
        }
        
        # 设置Cookie
        response = Response(response_data)
        response.set_cookie(
            key='token',  # Cookie的键
            value=str(token),  # Cookie的值
            max_age=604800,  # Cookie的有效期（单位：秒），这里设置为7天
            secure=False,  # 如果为True，则Cookie将通过HTTPS传输
            httponly=True,  # 如果为True，则Cookie将不会被JavaScript访问
            samesite='Lax'  # 设置SameSite属性，防止CSRF攻击
        )
        
        return response
    
class UserInfoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 用户信息可以从request.user获取，这里我们简单返回用户名
        username = request.user.username
        # 您可以在这里添加更多的用户信息，例如用户的头像链接等
        # user_avatar = 'https://example.com/avatar.png'

        return Response({
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": {
                "name": username,
                # "avatar": user_avatar,
            }
        })
