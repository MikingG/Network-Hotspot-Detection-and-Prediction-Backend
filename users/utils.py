from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # 先让DRF处理异常，获取其标准响应
    response = exception_handler(exc, context)
    
    # 如果是认证错误且状态码为401，修改响应内容
    if isinstance(exc, AuthenticationFailed) and response is not None:
        response_data = {
            "success": False,
            "code": 50014,
            "message": "Token已过期，请重新登录",
        }
        
    
    return Response(response_data)
