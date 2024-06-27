import json
import os
from django.shortcuts import render
import pandas as pd
from crawl.models import CrawlBriefData

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from crawl.utils import get_csv_name

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
                'last_update_time': crawl_data.last_update_time,
                'number': crawl_data.number,
            }
            data_list.append(data)
        response_data = {
            "success": True,
            "code": 20000,
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
        source = request.GET['source']
        # print(request)
        crawl_data_dict, csv_names = get_csv_name()
        csv_file_path = ""
        encoding = "utf-8"
        for csv_name in csv_names:
            print("".format(csv_name))
            if csv_name == str.format("{}_中山大学", source) or csv_name == str.format("中山大学{}", source):
                csv_file_path = os.path.join(crawl_data_dict, csv_name+'.csv')
                if csv_name[-2] == '凰' or csv_name[-2] == '讯':
                    encoding = 'gb2312'
        
        if csv_file_path == "":
            response_data = {
                "success": False,
                "code": 20001,
                "message": source,
                "data": '',
            }
            return Response(response_data)
        else:
            df = pd.read_csv(csv_file_path, encoding=encoding, encoding_errors="ignore")
            json_data = df.to_json(orient='records')

            response_data = {
                "success": True,
                "code": 20000,
                "message": "成功",
                "data": json_data,
            }

            # 返回响应
            return Response(response_data)