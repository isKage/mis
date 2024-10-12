from django.urls import path, include
from web.views import account, home

urlpatterns = [

    # 注册和登录
    path("register/", account.register, name="register"),
    path("login/", account.login, name="login"),  # 用户名登录
    path("image/code/", account.image_code, name="image_code"),  # 验证码图片生成
    path("logout/", account.logout, name="logout"),  # 导航条退出

    # 首页
    path("index/", home.index, name="index"),

]
