from django.urls import path, include
from mis import settings
from django.conf.urls.static import static
from web.views import account, home, yolo, prefer, help, report, admin_user, event

urlpatterns = [

    # 注册和登录
    path("register/", account.register, name="register"),
    path("login/", account.login, name="login"),  # 用户名登录
    path("image/code/", account.image_code, name="image_code"),  # 验证码图片生成
    path("logout/", account.logout, name="logout"),  # 导航条退出

    path("myevent/", event.my_event, name="my_event"),
    path("event/delete/<int:event_id>/", event.event_delete, name="event_delete"),

    # 首页
    path("index/", home.index, name="index"),

    path("event/", event.event_list, name="event_list"),
    path("event/add/", event.event_add, name="event_add"),
    path('event/detail/<int:event_id>/', event.event_detail, name='event_detail'),

    # 图片识别
    path("yolo/index", yolo.index, name="yolo_index"),
    path("yolo/upload", yolo.upload_image, name="upload_image"),

    # 偏好信息
    path('prefer/', prefer.preference_view, name='preference'),

    # 用户列表
    path('admin/user/list', admin_user.user_list, name='user_list'),

    # 帮助文档
    path('help/zh/', help.help_doc_zh, name='help_zh'),
    path('help/en/', help.help_doc_en, name='help_en'),

    # 报告
    path('report/', report.report_pdf, name='report_pdf'),
]

# # 添加媒体文件的 URL 配置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
