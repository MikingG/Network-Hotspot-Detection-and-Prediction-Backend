from django_filters import FilterSet, filters
from tadmin.models import UserInfo


class UserInfoFilter(FilterSet):
    name = filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = UserInfo
        fields = ('username',)
