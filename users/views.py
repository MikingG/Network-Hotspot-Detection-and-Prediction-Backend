from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from users.serializers import MyTokenObtainPairSerializer


class LoginView(TokenObtainPairView):
    # 通过 Django REST framework 的序列化器机制间接完成
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # 创建了MyTokenObtainPairSerializer的一个实例，并将请求的数据传递给这个序列化器
        # 这个实例化过程是Django REST framework自动完成的，因为它知道LoginView的serializer_class属性被设置为MyTokenObtainPairSerializer
        serializer = self.get_serializer(data=request.data)
        try:
            # 调用了序列化器的is_valid()方法，会自动调用validate方法来验证请求数据
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            return Response({
                "success": False,
                "code": 20001,
                "message": "用户名或密码错误",
                "data": {},
            })
        
        token = serializer.validated_data.get('access')
        # 在access_token过期时，用来获取一个新的access_token而不需要用户重新登录
        # refresh_token = serializer.validated_data.get('refresh')
        
        response_data = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": {
                "token": str(token),
                # 当access_token过期时，客户端可以使用refresh_token向服务器发起请求
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
        user_avatar = "https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.ws.126.net%2F2021%2F1120%2F783a7b4ej00r2tvvx002fd200hs00hsg00hs00hs.jpg&thumbnail=660x2147483647&quality=80&type=jpg"

        return Response({
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": {
                "name": username,
                "avatar": user_avatar,
            }
        })
    
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        # 通常这里不需要做任何事情，因为JWT是无状态的
        # 但是可以返回一个成功的响应来指示客户端登出操作已完成
        return Response({
            "success": True,
            "code": 20000,
            "message": "成功登出",
            "data": {}
        })
