from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tadmin import views

router = DefaultRouter()
router.register('UserInfo', views.UserInfoViewSet, basename='UserInfo')

urlpatterns = [
]

urlpatterns += [
    path('', include(router.urls)),
]
