from django.db.models import Avg
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Provider, Contact
from rest_framework.decorators import action
from .serializers import SerializersProviderAll, SerializersProduct, SerializersProvider
import qrcode
import io
import base64
from .tasks import send_email
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend


class ObjectsViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = SerializersProvider
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contacts__country', 'products__id']
    serializer_action_classes = {
        'list': SerializersProviderAll
    }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_backends = self.filter_queryset(queryset)
        serializer = SerializersProviderAll(filter_backends, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @action(methods=['get'], detail=True, url_path='contacts')
    def send_qr_with_contacts(self, request, pk=None):
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

            send_email.delay("Contacts", qr_code_image_data, settings.EMAIL_HOST_USER, request.user.email)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='big_debt')
    def get(self, request):
        avg = Provider.objects.aggregate(avg=Avg('debt_to_provider'))
        providers = Provider.objects.filter(debt_to_provider__gt=avg['avg'])
        serializer = SerializersProviderAll(providers, many=True)
        return Response(serializer.data)


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = SerializersProduct

