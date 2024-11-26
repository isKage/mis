from django.urls import path, include
from mis import settings
from django.conf.urls.static import static
from web.views import account, home, yolo, prefer

urlpatterns = [

    # 注册和登录
    path("register/", account.register, name="register"),
    path("login/", account.login, name="login"),  # 用户名登录
    path("image/code/", account.image_code, name="image_code"),  # 验证码图片生成
    path("logout/", account.logout, name="logout"),  # 导航条退出

    # 首页
    path("index/", home.index, name="index"),

    # 图片识别
    path("yolo/index", yolo.index, name="yolo_index"),
    path("yolo/upload", yolo.upload_image, name="upload_image"),

    # 偏好信息
    path('prefer/', prefer.preference_view, name='preference'),
]

# # 添加媒体文件的 URL 配置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)