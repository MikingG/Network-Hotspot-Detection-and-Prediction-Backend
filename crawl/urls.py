from django.urls import path
from crawl.views import BriefInfoView, DetailView

urlpatterns = [
    path('brief/', BriefInfoView.as_view(), name='brief'),
    path('detail/', DetailView.as_view(), name='detail'),
]