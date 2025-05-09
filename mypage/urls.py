from django.urls import path
from .views import InstanceListView, InstanceStatusUpdateView, InstanceDetailView

urlpatterns = [
    path('instances/', InstanceListView.as_view(), name='instance-list'),
    path('instances/<int:pk>/', InstanceDetailView.as_view(), name='instance-detail'),
    path('instances/<int:pk>/status/', InstanceStatusUpdateView.as_view(), name='instance-status-update'),
] 