from django.shortcuts import render
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import Product, Provider, Contact
from .serializers import SerializersProvider, SerializersProviderAll, SerializersProduct
from rest_framework.parsers import JSONParser


class Objects(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        providers = Provider.objects.all()
        serializer = SerializersProviderAll(providers, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = SerializersProvider(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def delete(self, request):
        id = request.data.get('id', None)
        try:
            Provider.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Products(APIView):

    def get(self, request):
        providers = Product.objects.all()
        serializer = SerializersProduct(providers, many=True)
        return Response(serializer.data)


    def post(self, request):
        data = request.data
        serializer = SerializersProduct(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def delete(self, request):
        id = request.data.get('id', None)
        try:
            Product.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ObjectsByCountryView(APIView):
    def get(self, request):
        country = request.query_params.get('country')
        providers = Provider.objects.filter(contacts__country=country)
        serializer = SerializersProviderAll(providers, many=True)
        return Response(serializer.data)


class ObjectsHaveHighDebt(APIView):
    def get(self, request):
        avg = Provider.objects.aggregate(avg=Avg('debt_to_provider'))
        providers = Provider.objects.filter(debt_to_provider__gt=avg['avg'])
        serializer = SerializersProviderAll(providers, many=True)
        return Response(serializer.data)


class ObjectsByProduct(APIView):
    def get(self, request):
        product_id = request.query_params.get('product_id')
        providers = Provider.objects.filter(products__id=product_id)
        serializer = SerializersProviderAll(providers, many=True)
        return Response(serializer.data)
