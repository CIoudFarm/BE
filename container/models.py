import uuid

from django.db import models
from django.utils import timezone
from container.tasks import update_functions_from_notes
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200")

class Container(models.Model):
    def default_functions():
        return ["해당 컨테이너에는 기능 설명이 없어요!"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='', null=True, blank=True)
    creater = models.CharField(max_length=100, default='', null=True, blank=True)
    scale = models.CharField(max_length=100, null=True, blank=True)
    hit_range = models.CharField(max_length=100, null=True, blank=True)
    electricity = models.CharField(max_length=100, null=True, blank=True)
    humid = models.CharField(max_length=100, null=True, blank=True)

    functions = models.JSONField(default=default_functions, null=True, blank=True)
    setting_file = models.JSONField(default=dict, null=True, blank=True)
    notes = models.CharField(max_length=1600, default='', null=True, blank=True)

    added_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    download_count = models.IntegerField(default=0, null=True, blank=True)
    stars = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return str(self.id)

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
