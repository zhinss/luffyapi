
from rest_framework.generics import ListAPIView
from django.conf import settings
from django.core.cache import cache

from home import serializers
from home import models


# 轮播图接口
class BannerListAPIView(ListAPIView):
    """轮播图接口"""
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('-order')[:settings.BANNER_COUNT]
    serializer_class = serializers.BannerModelSerializer

    def get(self, request, *args, **kwargs):

        banner_list = cache.get('banner_list')

        if not banner_list:
            response = self.list(request, *args, **kwargs)
            # response.data不是json数据，是drf中的自定义ReturnList类
            cache.set('banner_list', response.data)  # 缓存不设过期时间，更新任务交给celery异步任务框架
            return response

        return banner_list
