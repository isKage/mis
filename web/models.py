from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)  # db_index=True 创建索引，可以加快速度
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)

    def __str__(self):
        return self.username
