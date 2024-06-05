from django.contrib.auth.backends import ModelBackend
from users.models import UserInfo

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = UserInfo.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except UserInfo.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserInfo.objects.get(pk=user_id)
        except UserInfo.DoesNotExist:
            return None
