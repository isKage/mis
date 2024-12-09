"""
MD5加密
"""
import uuid
import hashlib
from django.conf import settings

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mis.settings")  # 替换 your_project 为你的项目名称
django.setup()  # 初始化 Django 环境


def md5(string):
    """MD5加密"""
    hash_object = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_object.update((string).encode('utf-8'))
    return hash_object.hexdigest()


def uid(string):
    data = "{}-{}".format(str(uuid.uuid4()), string)
    return md5(data)


if __name__ == '__main__':
    pwd = 'root123456'
    print(md5(pwd))
