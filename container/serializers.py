from rest_framework import serializers
from .models import Container


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 모든 필드를 required=False 로 설정
        for field in self.fields.values():
            field.required = False
