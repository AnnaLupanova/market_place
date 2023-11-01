from . import views
from django.urls import path, re_path
from .views import Objects, ObjectsHaveHighDebt, Products,GetQr, ObjectsByFilters

urlpatterns = [
    path('objects/filter/', ObjectsByFilters.as_view()),
    path('objects/high_debt/', ObjectsHaveHighDebt.as_view()),
    path('objects/<int:pk>/', Objects.as_view()),
    path('objects/<int:pk>/qr', GetQr.as_view()),
    path('objects/', Objects.as_view()),
    path('products/<int:pk>/', Products.as_view()),
    path('products/', Products.as_view()),

]