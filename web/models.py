from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)  # db_index=True 创建索引，可以加快速度
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)

    def __str__(self):
        return self.username


class Preference(models.Model):
    userid = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='关联用户id')
    student_id = models.CharField(max_length=20, verbose_name='学号')
    major = models.CharField(max_length=20, blank=True, null=True, verbose_name='专业')
    dorm_area = models.CharField(max_length=40, blank=True, null=True, verbose_name='宿舍')
    preferred_building = models.CharField(max_length=40, blank=True, null=True, verbose_name='偏好教学楼')
    preferred_subject = models.CharField(max_length=100, blank=True, null=True,  verbose_name='偏好学科')
    preferred_topic = models.CharField(max_length=100, blank=True, null=True, verbose_name='偏好话题')
    additional_preferences = models.CharField(max_length=100, blank=True, null=True, verbose_name='其他描述性偏好')