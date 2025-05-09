from rest_framework import viewsets
from .models import Container
from .serializers import ContainerSerializer

class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
