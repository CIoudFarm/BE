from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from farmdsl.views import CropSearchViewSet
from container.views import ContainerViewSet


router = DefaultRouter()
router.register(r"crops", CropSearchViewSet, basename="crops")
router.register(r'containers', ContainerViewSet)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("mypage/", include("mypage.urls")),
]

