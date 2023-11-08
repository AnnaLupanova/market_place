from django.urls import path, include
from rest_framework import routers
from .views import ObjectsViewSet, ProductsViewSet

router = routers.DefaultRouter()
router.register(r'objects', ObjectsViewSet)
router.register(r'products', ProductsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

