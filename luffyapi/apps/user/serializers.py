import re

from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from user import models


# 登陆序列化类
class LoginModelSerializer(serializers.ModelSerializer):
    """登陆序列化类"""
    username = serializers.CharField(min_length=3, max_length=32, write_only=True)
    password = serializers.CharField(min_length=3, max_length=16, write_only=True)

    class Meta:
        model = models.MyUser
        fields = ['username', 'password']

    # 全局校验钩子
    # 校验user, 签发token, 保存到serializer
    def validate(self, attrs):

        user = self._many_method_login(**attrs)

        # 签发token, 并将user和token存放在序列化对象中
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        self.user = user
        self.token = token

        return attrs

    # 多方式登陆
    def _many_method_login(self, **attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # 邮箱登陆
        if re.match(r'.*@.*', username):
            user = models.MyUser.objects.filter(email=username).first()

        # 手机号登陆
        elif re.match(r'^1[3-9][0-9]{9}$', username):
            user = models.MyUser.objects.filter(phone=username).first()

        # 普通账号登陆
        else:
            user = models.MyUser.objects.filter(username=username).first()

        if not user:
            raise serializers.ValidationError({'username': '账号错误'})

        if not user.check_password(password):
            raise serializers.ValidationError({'password': '密码错误'})

        return user
