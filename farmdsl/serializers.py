from rest_framework import serializers

class CropSearchSerializer(serializers.Serializer):
    crop_type = serializers.CharField()
    growing_period = serializers.CharField()
    budget = serializers.CharField()
    notes = serializers.CharField()