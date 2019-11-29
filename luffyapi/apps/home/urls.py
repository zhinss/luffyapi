from django.urls import path, re_path
from home import views

urlpatterns = [
    # 轮播图接口
    path('banner/', views.BannerListAPIView.as_view())
]
