from django.shortcuts import render, get_object_or_404
from rest_framework import generics, serializers
from .models import Instance
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status
from django.http import HttpResponse

class InstanceSerializer(serializers.ModelSerializer):
    base_config = serializers.FileField(write_only=True, required=False)
    class Meta:
        model = Instance
        fields = ['id', 'name', 'type', 'region', 'start_date', 'status', 'base_config', 'base_config_name']
        read_only_fields = ['start_date', 'status', 'base_config_name']

    def create(self, validated_data):
        # 파일 처리
        uploaded_file = self.context['request'].FILES.get('base_config')
        if uploaded_file:
            validated_data['base_config'] = uploaded_file.read()
            validated_data['base_config_name'] = uploaded_file.name
        else:
            validated_data['base_config'] = None
            validated_data['base_config_name'] = None
        # start_date/status 자동 저장
        validated_data['start_date'] = date.today()
        validated_data['status'] = '시작'
        return super().create(validated_data)

class InstanceListView(generics.ListCreateAPIView):
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer

class InstanceStatusUpdateView(APIView):
    def put(self, request, pk):
        instance = get_object_or_404(Instance, pk=pk)
        new_status = request.data.get('status')
        if new_status not in dict(Instance.STATUS_CHOICES):
            return Response({'detail': 'Invalid status.'}, status=drf_status.HTTP_400_BAD_REQUEST)
        instance.status = new_status
        if new_status == '시작':
            instance.start_date = date.today()
        instance.save()
        return Response({'id': instance.id, 'status': instance.status, 'start_date': instance.start_date}, status=drf_status.HTTP_200_OK)

class InstanceDetailView(generics.DestroyAPIView):
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer

class InstanceFileDownloadView(APIView):
    def get(self, request, pk):
        instance = get_object_or_404(Instance, pk=pk)
        if not instance.base_config:
            return Response({'detail': 'No file found.'}, status=drf_status.HTTP_404_NOT_FOUND)
        response = HttpResponse(instance.base_config, content_type='application/octet-stream')
        filename = instance.base_config_name or 'downloaded_file.json'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
