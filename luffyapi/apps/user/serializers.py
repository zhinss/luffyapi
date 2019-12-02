import re

from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.core.cache import cache
from django.conf import settings

from user import models
from libs.tx_sms.settings import CODE_LENGTH


# 多方式登陆序列化类
class LoginModelSerializer(serializers.ModelSerializer):
    """多方式登陆序列化类"""
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


# 手机号登陆序列化类
class PhoneLoginModelsSerializer(serializers.ModelSerializer):
    """手机号登陆序列化类"""
    phone = serializers.CharField(max_length=11, min_length=11, write_only=True)
    code = serializers.CharField(write_only=True, min_length=CODE_LENGTH, max_length=CODE_LENGTH)

    class Meta:
        model = models.MyUser
        fields = ['phone', 'code']

    # 局部钩子验证手机号是否合法
    def validate_phone(self, value):
        # 校验手机号
        if not (value and re.match(r'^1[3-9][0-9]{9}$', value)):
            raise serializers.ValidationError('请输入正确的手机号')

        return value

    # 局部钩子验证验证码是否合法
    def validate_code(self, value):
        # 校验验证码
        try:
            int(value)
        except:
            raise serializers.ValidationError('验证码错误')

        return value

    # 全局钩子签发token
    def validate(self, attrs):

        user = self._get_user(**attrs)

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        self.user = user
        self.token = token

        return attrs

    # 验证验证码获取用户
    def _get_user(self, **attrs):

        phone = attrs.get('phone')
        code = attrs.get('code')

        user = models.MyUser.objects.filter(phone=phone).first()

        if not user:
            raise serializers.ValidationError({'phone': '用户未注册'})

        # 获取缓存中的验证码
        # true_code = cache.get(settings.SMS_CACHE_KEY % phone)
        true_code = '123456'

        if code != true_code:
            raise serializers.ValidationError({'code': '验证码错误'})

        return user


# 手机号注册序列化类
class RegisterModelSerializer(serializers.ModelSerializer):
    """手机号注册序列化类"""

    code = serializers.CharField(max_length=CODE_LENGTH, min_length=CODE_LENGTH, write_only=True)

    class Meta:
        model = models.MyUser
        fields = ['phone', 'password', 'code']
        extra_kwarg = {
            'phone': {
                'min_length': 11,
                'max_length': 11,
            },
            'password': {
                'min_length': 6,
                'max_length': 16,
            }
        }

    def validate_phone(self, value):

        if not re.match(r'^1[3-9][0-9]{9}$', value):
            raise serializers.ValidationError('请输入正确的手机号')

        return value

    def validate_code(self, value):
        try:
            int(value)
            return value
        except:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.pop('code')

        user = models.MyUser.objects.filter(phone=phone).first()

        if user:
            raise serializers.ValidationError({'phone': '手机号已注册'})

        # true_code = cache.get(settings.SMS_CACHE_KEY % phone)
        true_code = '123456'
        if code != true_code:
            raise serializers.ValidationError({'code': '验证码错误'})

        attrs['username'] = phone
        attrs['email'] = phone + '@163.com'

        return attrs

    def create(self, validated_data):
        return models.MyUser.objects.create_user(**validated_data)

