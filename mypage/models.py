from django.db import models


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

    name = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)
    base_config = models.BinaryField(null=True, blank=True)
    base_config_name = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name or ""
