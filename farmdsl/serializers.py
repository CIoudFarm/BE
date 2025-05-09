from rest_framework import serializers

class CropSearchSerializer(serializers.Serializer):
    crop_type = serializers.CharField(required=False, allow_blank=True)
    growing_period = serializers.IntegerField(required=False)
    budget = serializers.IntegerField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    container = serializers.JSONField(required=False)
