import re

from rest_framework.views import APIView
from django.conf import settings
from django.core.cache import cache

from user import models, serializers, throttles
from utils.response import APIResponse
from libs import tx_sms


# 多方式登陆接口
class LoginAPIView(APIView):
    """多方式登陆接口"""
    def post(self, request, *args, **kwargs):
        # 反序列化
        serializer = serializers.LoginModelSerializer(data=request.data)
        # 校验数据
        serializer.is_valid(raise_exception=True)

        return APIResponse(data={
            'username': serializer.user.username,
            'token': serializer.token
        })


# 手机注册验证
class MobileAPIView(APIView):
    """手机注册验证"""
    def post(self, request, *args, **kwargs):
        # 获取前台传过来手机号
        phone = request.data.get('phone')

        # 校验手机号
        if not (phone and re.match(r'^1[3-9][0-9]{9}$', phone)):
            return APIResponse(2, '手机号格式有误')

        try:
            # 已经注册了
            models.MyUser.objects.get(phone=phone)
            return APIResponse(1, '手机号已被注册')
        except:
            # 没有注册过
            return APIResponse(0, '手机未注册')


# 发送短信验证码接口
class SMSAPIView(APIView):
    """发送短信验证码接口"""
    throttle_classes = [throttles.SMSRateThrottle]

    def post(self, request, *args, **kwargs):
        # 拿到前台传过来的手机号
        phone = request.data.get('phone')
        if not (phone and re.match(r'^1[3-9][0-9]{9}$', phone)):
            return APIResponse(2, '手机号格式有误')

        # 获取验证码
        code = tx_sms.get_code()
        # 发送短信
        result = tx_sms.send_sms(phone, code, settings.SMS_EXP // 60)
        # 服务器缓存验证码
        if not result:
            return APIResponse(1, '发送验证码失败')
        cache.set(settings.SMS_CACHE_KEY % phone, code, settings.SMS_EXP)

        # 校验发送的验证码与缓存的验证码是否一致
        print('>>>>> %s - %s <<<<<' % (code, cache.get(settings.SMS_CACHE_KEY % phone)))

        return APIResponse(0, '发送验证码成功')


# 手机号登陆
class CodeLoginAPIView(APIView):
    """手机号登陆"""
    def post(self, request, *args, **kwargs):

        user_ser = serializers.PhoneLoginModelsSerializer(data=request.data)

        user_ser.is_valid(raise_exception=True)

        return APIResponse(data={
            'username': user_ser.user.username,
            'token': user_ser.token
        })


# 手机注册
class RegisterAPIView(APIView):
    """手机注册"""
    def post(self, request, *args, **kwargs):

        user_ser = serializers.RegisterModelSerializer(data=request.data)

        user_ser.is_valid(raise_exception=True)
        user = user_ser.save()

        return APIResponse(msg='注册成功', data={
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
        })






