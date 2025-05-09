import uuid

from django.db import models
from django.utils import timezone
from container.tasks import update_functions_from_notes
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

class Container(models.Model):
    def default_functions():
        return ["해당 컨테이너에는 기능 설명이 없어요!"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ✅ UUID 기반 ID
    name = models.CharField(max_length=100, default='')
    creater = models.CharField(max_length=100, default='')
    scale = models.CharField(max_length=100)
    hit_range = models.CharField(max_length=100)
    electricity = models.CharField(max_length=100)
    humid = models.CharField(max_length=100)

    functions = models.JSONField(default=default_functions) # 리스트[str] 저장용 (SQLite에서는 JSONField 사용 가능 in Django 3.1+)
    setting_file = models.JSONField(default=dict)  # 복잡한 설정 저장
    notes = models.CharField(max_length=1600, default='')

    added_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    download_count = models.IntegerField(default=0)
    stars = models.FloatField(default=0.0)
   
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_create = self.pk is None
        result = super().save(force_insert, force_update, using, update_fields)

        if is_create:
            try:
                es.index(index="crops", 
                    id=str(self.pk), 
                    body={
                        "container": str(self.pk),
                        "notes": self.notes,
                    }
                )
            except Exception as e:
                print(f"❌ Elasticsearch 색인 실패: {e}")

            update_functions_from_notes.delay(self.pk)

        return result
