from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# 用户表
class MyUser(AbstractUser):
    """用户表"""
    phone = models.CharField(max_length=11, verbose_name='手机号', null=True, blank=True)
    image = models.ImageField(upload_to='user/%Y/%m', verbose_name='头像', default='media/user/卡卡西.jpg', blank=True)

    class Meta:
        db_table = 'luffy_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username


# 轮播图
class Banner(models.Model):
    """轮播图"""
    order = models.IntegerField(verbose_name='显示顺序')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图', blank=True)
    url = models.URLField()

    class Meta:
        db_table = 'luffy_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'图片{self.order}'
