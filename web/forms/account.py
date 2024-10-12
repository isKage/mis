from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings

import random

from web import models
from web.forms.bootstrap import BootStrapForm
from utils import encrypt


class RegisterModelForm(BootStrapForm, forms.ModelForm):
    """用户注册"""
    username = forms.CharField(
        label='用户名',
        min_length=2,
        max_length=25,
        error_messages={
            'min_length': "用户名长度不能小于2个字符",
            'max_length': "用户名长度不能大于2个字符"
        },
        widget=forms.TextInput()
    )

    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "密码长度不能小于8个字符",
            'max_length': "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='重复密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "重复密码长度不能小于8个字符",
            'max_length': "重复密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput()
    )

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password']

    # 用户名不能重复
    def clean_username(self):
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(username=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        return encrypt.md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])

        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')

        return confirm_pwd


class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='用户名或邮箱')
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    code = forms.CharField(label='图片验证码')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        return encrypt.md5(pwd)

    def clean_code(self):
        """ 钩子 图片验证码是否正确？ """
        # 读取用户输入的验证码
        code = self.cleaned_data['code']

        # 去session获取自己的验证码
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')

        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入错误')

        return code
