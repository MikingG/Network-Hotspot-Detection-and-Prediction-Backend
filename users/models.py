from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
# from .managers import CustomUserManager  # 确保你创建了一个自定义的用户管理器
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    自定义用户模型管理器，使用用户名作为唯一标识符，并支持密码的创建。
    """

    def create_user(self, username, password=None, **extra_fields):
        """
        创建并保存一个具有给定用户名和密码的用户。
        """
        if not username:
            raise ValueError(_('The Username must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        创建并保存一个超级用户。
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)
    
class UserInfo(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('用户名'), max_length=128, primary_key=True, unique=True)
    password = models.CharField(_('密码'), max_length=128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()  # 使用自定义的用户管理器

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # 如果有其他必填字段，请在这里添加

    class Meta:
        verbose_name = _('用户信息')
        verbose_name_plural = _('用户信息')

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return self.password == raw_password
    


