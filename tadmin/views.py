from rest_framework.viewsets import ModelViewSet
from tadmin.models import UserInfo
from tadmin.serializer import UserInfoSerializer
from tadmin.filter import UserInfoFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserInfoViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    filter_class = UserInfoFilter
    filter_fields = ['username',]
    search_fields = ('username',)
