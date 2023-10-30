from django.shortcuts import render
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Provider, Contact
from .serializers import SerializersProvider, SerializersProviderAll, SerializersProduct
from rest_framework.parsers import JSONParser



class Objects(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        providers = Provider.objects.all()
        serializer = SerializersProviderAll(providers, many=True)
        providers = Provider.objects.filter(parent__isnull=False)
        for i in providers:
            print(i.name)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SerializersProvider(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Provider.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = SerializersProvider(data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        try:
            Provider.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error": "Object does not exists"})


class Products(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get(self, request):
        providers = Product.objects.all()
        serializer = SerializersProduct(providers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SerializersProduct(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Product.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = SerializersProduct(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        try:
            Product.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error": "Object does not exists"})


class ObjectsByCountryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        country = request.query_params.get('country')
        providers = Provider.objects.filter(contacts__country=country)
        serializer = SerializersProviderAll(providers, many=True)
        return Response(serializer.data)


class ObjectsHaveHighDebt(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        avg = Provider.objects.aggregate(avg=Avg('debt_to_provider'))
        providers = Provider.objects.filter(debt_to_provider__gt=avg['avg'])
        serializer = SerializersProviderAll(providers, many=True)
        return Response(serializer.data)


class ObjectsByProduct(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        product_id = request.query_params.get('product_id')
        providers = Provider.objects.filter(products__id=product_id)
        serializer = SerializersProviderAll(providers, many=True)
        return Response(serializer.data)
