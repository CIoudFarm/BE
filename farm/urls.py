from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from farmdsl.views import CropSearchViewSet


router = DefaultRouter()
router.register(r"crops", CropSearchViewSet, basename="crops")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]

