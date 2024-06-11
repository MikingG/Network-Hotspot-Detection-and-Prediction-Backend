from django.shortcuts import render
from crawl.models import CrawlBriefData

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class BriefInfoView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = []

    def get(self, request):
        # 构造响应数据
        brief_infos = CrawlBriefData.objects.all()
        data_list = []
        for crawl_data in brief_infos:
            data = {
                'no': crawl_data.no,
                'name': crawl_data.name,
                'last_update_time': crawl_data.last_update_time.isoformat(),
                'number': crawl_data.number,
            }
            data_list.append(data)
        response_data = {
            "success": True,
            "code": 200,
            "message": "成功",
            "data": data_list,
        }

        # 返回响应
        return Response(response_data)

class DetailView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = []

    def get(self, request):
        # 构造响应数据
        response_data = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": {
                
            }
        }

        # 返回响应
        return Response(response_data)