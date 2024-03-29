from django.urls import path, re_path
from user import views

urlpatterns = [
    # 多方式登陆接口
    path('login', views.LoginAPIView.as_view()),
    # 验证手机号接口
    path('mobile', views.MobileAPIView.as_view()),
    # 发送短信
    path('sms', views.SMSAPIView.as_view()),
    # 验证码登陆
    path('login/code', views.CodeLoginAPIView.as_view()),
    # 注册
    path('register', views.RegisterAPIView.as_view()),

]
