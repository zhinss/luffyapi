from rest_framework.views import APIView
from utils.response import APIResponse
from user import models, serializers


# 用户接口
class UserAPIView(APIView):
    """用户接口"""
    def get(self, request, *args, **kwargs):

        return APIResponse(results={'haha'})


# 轮播图接口
class BannerAPIView(APIView):
    """轮播图接口"""
    def get(self, request, *args, **kwargs):

        banner_obj = models.Banner.objects.all().order_by('order')[:3]

        banner_ser = serializers.BannerModelSerializer(banner_obj, many=True, context={'request': request})

        return APIResponse(results=banner_ser.data)

