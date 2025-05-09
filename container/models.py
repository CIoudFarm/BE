from django.db import models
from django.utils import timezone
# from django.contrib.postgres.fields import ArrayField  # PostgreSQL용 → SQLite에선 List 저장은 TextField + JSON 직렬화 필요
# import json


class Container(models.Model):
    scale = models.CharField(max_length=100)
    hit_range = models.CharField(max_length=100)
    electricity = models.CharField(max_length=100)
    humid = models.CharField(max_length=100)

    functions = models.JSONField(default=list)  # 리스트[str] 저장용 (SQLite에서는 JSONField 사용 가능 in Django 3.1+)
    setting_file = models.JSONField(default=dict)  # 복잡한 설정 저장

    added_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    download_count = models.IntegerField(default=0)
    stars = models.FloatField(default=0.0)

    def __str__(self):
        return f"Container {self.id} ({self.scale})"
