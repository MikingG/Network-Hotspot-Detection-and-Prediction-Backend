from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # 先让DRF处理异常，获取其标准响应
    response = exception_handler(exc, context)

    # 确保在utils.py中的custom_exception_handler函数处理所有可能的异常情况，并且总是定义response_data变量。
    if response is not None:
        response_data = {
            'success': False,
            'code': response.status_code,
            'message': str(exc.detail),
        }
    # 如果是认证错误且状态码为401，修改响应内容
    elif isinstance(exc, AuthenticationFailed) and response is not None:
        response_data = {
            "success": False,
            "code": 50014,
            "message": "Token已过期，请重新登录",
        }
    else:
        response_data = {
            'success': False,
            'code': 50000,
            'message': 'Internal server error'
        }
        
    
    return Response(response_data)
