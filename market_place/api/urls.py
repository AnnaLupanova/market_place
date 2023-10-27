from . import views
from django.urls import path, re_path
from .views import Objects, ObjectsByCountryView, ObjectsHaveHighDebt, ObjectsByProduct, Products

urlpatterns = [
    path('objects/filter/', ObjectsByCountryView.as_view()),
    path('objects/high_debt/', ObjectsHaveHighDebt.as_view()),
    path('objects/product/', ObjectsByProduct.as_view()),
    path('objects/', Objects.as_view()),
    path('products/', Products.as_view()),



   # path('<country>/', GetProvidersByCountry.as_view())

]