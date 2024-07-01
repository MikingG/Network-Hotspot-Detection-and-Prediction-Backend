from django.urls import path
from users.views import LoginView, UserInfoView, LogoutView, getHotspotsView, getCategoryView, getWordFrequencyView,getEventListView,getTrendFrequencyView, getTrendRankingView,getTrendHotspotView,\
                        addUserView,deleteUserView,updateUserView,getAllUserView,isStaffView,changeAdminView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('getHotspots/', getHotspotsView.as_view(), name='getHotspots'),
    path('getCategory/', getCategoryView.as_view(), name='getCategory'),
    path('getWordFrequency/', getWordFrequencyView.as_view(), name='getWordFrequency'),
    path('geteventlist/', getEventListView.as_view(), name='geteventlist'),
    path('getTrendWordFrequency/', getTrendFrequencyView.as_view(), name='getTrendWordFrequency'),
    path('getTrendRanking/', getTrendRankingView.as_view(), name='getTrendRanking'),
    path('getTrendHotspots/', getTrendHotspotView.as_view(), name='getTrendHotspot'),
    path('addUser/', addUserView.as_view(), name='add_user'),
    path('deleteUser/', deleteUserView.as_view(), name='delete_user'),
    path('updateUser/', updateUserView.as_view(), name='update_user'),
    path('getAllUser/', getAllUserView.as_view(), name='get_all_user'),
    path('changeAdmin/', changeAdminView.as_view(), name='get_all_user'),
    path('isStaff/',isStaffView.as_view(),name='isStaff')
]