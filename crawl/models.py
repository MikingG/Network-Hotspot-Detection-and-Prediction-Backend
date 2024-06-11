from django.db import models



# Create your models here.
class CrawlBriefData(models.Model):
    no = models.AutoField(primary_key=True)  # 自增主键字段
    name = models.CharField(max_length=200, default='', blank=True)  # 名称字段，假设最大长度为200，可以为空
    last_update_time = models.CharField(max_length=200, default='', blank=True)  # 最后更新时间字段，每次保存对象时自动设置为当前时间
    number = models.IntegerField(default=0)  # 数字字段，假设默认值为0

class CrawlDetailData(models.Model):
    no = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
