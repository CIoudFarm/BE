from django.db import models

# Create your models here.

class Instance(models.Model):
    TYPE_CHOICES = [
        ("기본형", "기본형"),
        ("표준형", "표준형"),
        ("고급형", "고급형"),
    ]
    STATUS_CHOICES = [
        ("시작", "시작"),
        ("중지됨", "중지됨"),
    ]
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    base_config = models.FileField(upload_to='base_configs/', null=True, blank=True)
    region = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
