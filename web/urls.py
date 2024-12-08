from django.urls import path, include
from mis import settings
from django.conf.urls.static import static
from web.views import account, home, yolo, prefer, help, report, admin_user, event, group

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
    path('event/<int:event_id>/article/new/', event.article_create, name='article_create'),  # 新建文章
    path('article/<int:article_id>/edit/', event.article_edit, name='article_edit'),  # 编辑文章
    path('article/delete/<int:article_id>/', event.article_delete, name='article_delete'),
    path('article/<int:article_id>/summarize/', event.summarize_article, name='article_summarize'),  # 总结文章

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

    # 小组
    path('groups/', group.group_list, name='group_list'),
    path('groups/add/', group.group_add, name='group_add'),
    path('groups/join/<int:group_id>/', group.group_join_request, name='group_join_request'),
    path('groups/requests/', group.membership_requests, name='membership_requests'),
    path('groups/requests/approve/<int:request_id>/', group.approve_request, name='approve_request'),
    path('groups/delete/<int:group_id>/', group.delete_group, name='group_delete'),
    path('groups/leave/<int:group_id>/', group.group_leave, name='group_leave'),
]

# # 添加媒体文件的 URL 配置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
