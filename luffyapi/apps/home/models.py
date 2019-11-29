from django.db import models
from utils.models import BaseModel
# Create your models here.


# 轮播图
class Banner(BaseModel):
    """轮播图"""
    title = models.CharField(max_length=32, verbose_name='图片名')
    order = models.IntegerField(verbose_name='显示顺序')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图', blank=True)
    link = models.CharField(max_length=256)

    class Meta:
        db_table = 'luffy_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
