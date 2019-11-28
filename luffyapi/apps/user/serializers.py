from rest_framework import serializers
from user import models


# 轮播图序列化类
class BannerModelSerializer(serializers.ModelSerializer):
    """轮播图序列化类"""
    class Meta:
        model = models.Banner
        fields = ['image']
