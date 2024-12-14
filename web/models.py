from django.db import models
from django.utils.timezone import now


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)  # db_index=True 创建索引，可以加快速度
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Preference(models.Model):
    userid = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='关联用户id')
    student_id = models.CharField(max_length=20, verbose_name='学号')
    major = models.CharField(max_length=20, blank=True, null=True, verbose_name='专业')
    dorm_area = models.CharField(max_length=40, blank=True, null=True, verbose_name='宿舍')
    preferred_building = models.CharField(max_length=40, blank=True, null=True, verbose_name='偏好教学楼')
    preferred_subject = models.CharField(max_length=100, blank=True, null=True, verbose_name='偏好学科')
    preferred_topic = models.CharField(max_length=100, blank=True, null=True, verbose_name='偏好话题')
    additional_preferences = models.CharField(max_length=100, blank=True, null=True, verbose_name='其他描述性偏好')
    recommendation_text = models.TextField(null=True, blank=True)  # 新增字段存储推荐文本

    def __str__(self):
        return self.userid.username


class Event(models.Model):
    TOPIC_TYPE = [
        ('team', '团队发起'),
        ('individual', '个人发起'),
    ]

    topic_name = models.CharField(max_length=200, verbose_name="话题名称")  # 话题名称
    topic_description = models.TextField(verbose_name="话题简介")  # 话题简介
    initiator = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name="events", verbose_name="发起者"
    )  # 发起者，连接到 UserInfo 表
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  # 创建时间
    participants = models.PositiveIntegerField(default=1, verbose_name="参与人数")  # 参与人数
    topic_type = models.CharField(
        max_length=10, choices=TOPIC_TYPE, verbose_name="发起类型"
    )  # 团队发起/个人发起

    def __str__(self):
        return self.topic_name


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="文章标题")
    content = models.TextField(verbose_name="文章内容")  # Markdown 内容
    creator = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name="articles", verbose_name="创建者"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="articles", verbose_name="所属事件"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.title


class Group(models.Model):
    group_name = models.CharField(max_length=100, verbose_name="小组名称")
    description = models.TextField(verbose_name="小组简介", blank=True)
    creator = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name="created_groups", verbose_name="创建者"
    )
    members = models.ManyToManyField(UserInfo, related_name="joined_groups", verbose_name="小组成员")
    created_at = models.DateTimeField(default=now, verbose_name="小组创建时间")
    topic = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,  # 删除话题时将 topic 设为 NULL
        related_name="related_groups",
        verbose_name="关联话题",
        null=True,
        blank=True,  # 表示此字段可以为空
    )

    def __str__(self):
        return self.group_name


class MembershipRequest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="membership_requests")
    applicant = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="sent_requests")
    reason = models.TextField(verbose_name="申请理由")
    status = models.CharField(
        max_length=10,
        choices=[('pending', '待处理'), ('approved', '已同意'), ('rejected', '已拒绝')],
        default='pending',
        verbose_name="状态",
    )
    created_at = models.DateTimeField(default=now, verbose_name="申请时间")

    def __str__(self):
        return f"{self.applicant.username} -> {self.group.group_name} ({self.status})"
