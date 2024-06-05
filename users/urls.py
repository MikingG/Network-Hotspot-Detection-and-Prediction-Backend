from django.urls import path
from users.views import LoginView, UserInfoView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('info/', UserInfoView.as_view(), name='user_info'),
]
