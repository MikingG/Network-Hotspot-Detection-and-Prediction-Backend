
from neo4j import GraphDatabase
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from users.serializers import MyTokenObtainPairSerializer

import csv
import math
import os
import random
import pandas as pd



#---------- 登录退出系统 ----------#

class LoginView(TokenObtainPairView):
    # 通过 Django REST framework 的序列化器机制间接完成
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # 创建了MyTokenObtainPairSerializer的一个实例，并将请求的数据传递给这个序列化器
        # 这个实例化过程是Django REST framework自动完成的，因为它知道LoginView的serializer_class属性被设置为MyTokenObtainPairSerializer
        serializer = self.get_serializer(data=request.data)
        try:
            # 调用了序列化器的is_valid()方法，会自动调用validate方法来验证请求数据
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            return Response({
                "success": False,
                "code": 20001,
                "message": "用户名或密码错误",
                "data": {},
            })
        
        token = serializer.validated_data.get('access')
        # 在access_token过期时，用来获取一个新的access_token而不需要用户重新登录
        refresh_token = serializer.validated_data.get('refresh')
        
        response_data = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": {
                "token": str(token),
                # 当access_token过期时，客户端可以使用refresh_token向服务器发起请求
                "refresh_token": str(refresh_token),
            }
        }
        
        # 设置Cookie
        response = Response(response_data)
        response.set_cookie(
            key='token',  # Cookie的键
            value=str(token),  # Cookie的值
            max_age=604800,  # Cookie的有效期（单位：秒），这里设置为7天
            secure=False,  # 如果为True，则Cookie将通过HTTPS传输
            httponly=True,  # 如果为True，则Cookie将不会被JavaScript访问
            samesite='Lax'  # 设置SameSite属性，防止CSRF攻击
        )
        
        return response
    

class UserInfoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 由于我们使用了IsAuthenticated权限，我们可以直接从request.user获取用户信息
        username = request.user.username
        print(username)
        # 这里可以添加更多的用户信息，例如用户的头像链接等
        user_avatar = "https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.ws.126.net%2F2021%2F1120%2F783a7b4ej00r2tvvx002fd200hs00hsg00hs00hs.jpg&thumbnail=660x2147483647&quality=80&type=jpg"

        # 构造响应数据
        response_data = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": {
                "name": username,
                "avatar": user_avatar,
            }
        }

        # 返回响应
        return Response(response_data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # 通常这里不需要做任何事情，因为JWT是无状态的
        # 但是可以返回一个成功的响应来指示客户端登出操作已完成
        return Response({
            "success": True,
            "code": 20000,
            "message": "成功登出",
            "data": {}
        })

#---------------------------------#



#---------- 数据基本分析 ----------#

class getHotspotsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = []
        file_path = os.path.join('data', 'key_info.csv')
        # 读取key_info.csv文件，提取Event Title和Number of news items字段
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                hotspot = row['Event Title']
                score = int(row['Number of news items'])
                transformed_score = math.log(score + 2)  # 使用自然对数
                random_noise = random.uniform(-0.5, 0.5)  # 生成一个范围在-5到5之间的随机数
                final_score = transformed_score + random_noise
                # 将提取的数据添加到data列表中
                data.append({'hotspot': hotspot, 'score': final_score})
        # 构造响应数据
        response_data = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": data
        }
        return Response(response_data)


class getCategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        file_path = os.path.join('data', 'key_info.csv')
        key_info = pd.read_csv(file_path, encoding='utf-8')
        # 按类别分组并计算每个类别的新闻数量之和
        grouped_data = key_info.groupby('Event Category')['Number of news items'].sum().reset_index()
        # 计算总和
        total_value = grouped_data['Number of news items'].sum()
        # 构建响应数据
        data = [{'name': category, 'value': round(value / total_value * 100, 2)} 
                for category, value in zip(grouped_data['Event Category'], grouped_data['Number of news items'])]
        
        response_data = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": data
        }
        return Response(response_data)


class getWordFrequencyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        words = []
        values = []
        file_path = os.path.join('data', 'word_frequencies.csv')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            words = next(reader)
            values = next(reader)
        
        # 将值转换为整数
        values = [int(value) for value in values]
        
        # 创建数据字典
        word_frequencies = [{'name': word, 'value': value} for word, value in zip(words, values)]
        
        response_data = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": word_frequencies
        }
        
        return Response(response_data)

#---------------------------------#



#------------ 事件图谱 ------------#

class getEventListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        URI = "bolt://localhost:7687"
        AUTH = ("admin", "0527")
        with GraphDatabase.driver(URI, auth=AUTH) as client:
            session = client.session(database="eventgraph1")
            ret = session.run("match (n:抽象事件) return n")
            event_list = []
            for item in ret.data():
                event_list.append(item['n']['name'])
            
            # 构建响应数据
            response_data = {
                "success": True,
                "code": 20000,
                "message": "成功",
                "data": event_list
                }
            return Response(response_data)
            # 构建响应数据
            # return Response({
            #     'success': True,
            #     'code': 20000,
            #     'message': 'success',
            #     'data': event_list
            # })
        

class getEventGraphView(APIView):
    def post(self, request):
        # 获取请求参数
        event_name = request.data.get('event_name')

#---------------------------------#



#------------ 热点预测 ------------#

class getTrendFrequencyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        word_frequencies = []
        file_path = os.path.join('trend_prediction/data', 'tiktok_中山大学_05_keyword_counts.csv')

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过表头
            
            for keyword, total_count in reader:
                # 直接读取关键字和计数，无需转换，因为它们已经是预期的格式
                word_frequencies.append({'name': keyword, 'value': int(total_count)})
        
        response_data = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": word_frequencies
        }
        
        return Response(response_data)
    

class getTrendHotspotView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        word_frequencies = []
        total_sum = 0  # 用于累加所有的sample_count
        file_path = os.path.join('trend_prediction/data', 'tiktok_中山大学_06_cluster_keywords_topics.csv')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过表头
            
            # 第一次遍历以计算总频数和
            for _, sample_count_str in reader:
                sample_count = int(sample_count_str)
                total_sum += sample_count
                
            # 将文件指针重置到开始，以便再次遍历
            f.seek(0)
            next(reader)  # 再次跳过表头
            
            # 第二次遍历以计算百分比
            for topic, sample_count_str in reader:
                sample_count = int(sample_count_str)
                # 计算百分比
                percent = (sample_count / total_sum) * 100 if total_sum != 0 else 0
                word_frequencies.append({'hotspot': topic, 'score': round(percent, 2)})
        
        response_data = {
            "success": True,
            "code": 20000,
            "message": "成功",
            "data": word_frequencies
        }
        
        return Response(response_data)

#---------------------------------#