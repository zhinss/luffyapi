from django.urls import path, re_path
from user import views

urlpatterns = [
    path('api/', views.UserAPIView.as_view()),

    path('banner/', views.BannerAPIView.as_view())
]
