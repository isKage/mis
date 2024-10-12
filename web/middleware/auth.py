import datetime
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from web import models


class MIS(object):

    def __init__(self):
        self.user = None


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """ 如果用户已登录，则request中赋值 """
        request.mis = MIS()

        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.mis.user = user_object

        # 白名单：没有登录都可以访问的URL
        """
        1. 获取当用户访问的URL
        2. 检查URL是否在白名单中，如果在，则可以继续向后访问，如果不在则进行判断是否已登录
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:  # 返回None表示通过中间件
            return

        # 检查用户是否已登录，已登录继续往后走；未登录则返回登录页面。
        if not request.mis.user:
            return redirect('login')
