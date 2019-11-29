from rest_framework.generics import ListAPIView
from home import serializers
from home import models


# 轮播图接口
class BannerListAPIView(ListAPIView):
    """轮播图接口"""
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('-order')[:4]
    serializer_class = serializers.BannerModelSerializer
