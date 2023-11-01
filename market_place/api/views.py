from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Provider, Contact, Employee
from .serializers import SerializersProvider, SerializersProviderAll, SerializersProduct
from rest_framework.parsers import JSONParser
import qrcode
import io
import base64
from .tasks import send_email_fun
from django.conf import settings


class GetQr(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        contact = Contact.objects.filter(company_id=pk)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        data = ','.join(map(str, contact))
        qr.add_data(data)
        qr.make(fit=True)

        qr_code_image = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        buffer = io.BytesIO()
        qr_code_image.save(buffer, format="PNG")
        qr_code_image_data = base64.b64encode(buffer.getvalue()).decode()
        try:
            send_email_fun.delay("Contacts", qr_code_image_data, settings.EMAIL_HOST_USER, request.user.email)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Objects(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_company_id = Employee.objects.filter(user__username=request.user.username).values_list('company')[0][0]
        providers = Provider.objects.filter(id=user_company_id)
        serializer = SerializersProviderAll(providers, many=True)
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
        providers = Provider.objects.filter(contacts__country__iexact=country)
        serializer = SerializersProviderAll(providers, many=True)
        return Response(serializer.data)


class ObjectsHaveHighDebt(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        avg = Provider.objects.aggregate(avg=Avg('debt_to_provider'))
        providers = Provider.objects.filter(debt_to_provider__gt=avg['avg'])
        serializer = SerializersProviderAll(providers, many=True)
        return Response(serializer.data)


class ObjectsByFilters(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        country = request.query_params.get('country', None)
        product_id = request.query_params.get('product_id', None)
        if country:
            providers = Provider.objects.filter(contacts__country__iexact=country)
            serializer = SerializersProviderAll(providers, many=True)
            return Response(serializer.data)
        elif product_id:
            providers = Provider.objects.filter(products__id=product_id)
            serializer = SerializersProviderAll(providers, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)
