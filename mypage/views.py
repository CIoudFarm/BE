from django.shortcuts import render, get_object_or_404
from rest_framework import generics, serializers
from .models import Instance
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status

class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = ['id', 'name', 'type', 'region', 'start_date', 'status', 'base_config']
        read_only_fields = ['start_date', 'status']

    def create(self, validated_data):
        # start_date는 오늘 날짜, status는 '시작'으로 자동 저장
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
