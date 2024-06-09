from rest_framework import serializers
from users.models import UserInfo
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 在这里您可以添加自定义的claims
        token['username'] = user.username
        return token

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = UserInfo.objects.filter(username=username).first()
        print("user",user)
        if user is None:
            raise AuthenticationFailed('用户名不存在', code='authorization')

        if not user.check_password(password):
            raise AuthenticationFailed('密码错误', code='authorization')
        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserInfo(username=validated_data['username'], password=validated_data['password'])
        user.set_password(validated_data['password'])  # 使用 set_password 方法
        user.save()
        return user
