from django.db import models
from django.conf import settings
# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending','未完成'),
        ('completed','已完成'),
    ]

    PRIORITY_CHOICES = [
        ('low','低'),
        ('medium','中'),
        ('high','高'),
    ]

    title = models.CharField(max_length=255,verbose_name="任务标题")
    description = models.TextField(blank=True,verbose_name="任务内容")
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending',verbose_name='任务状态')
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES,default='medium',verbose_name='任务优先级')

    created_at = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='所属用户'
    )

    def __str__(self):
        return self.title
