from rest_framework import serializers
from .models import Provider, Product, Employee, Contact
from datetime import datetime
from django.contrib.auth.models import User


class SerializersContact(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('email', 'country', 'city', 'street', 'building_number')


class SerializersEmployee(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user.username")
    email = serializers.CharField(read_only=True, source="user.email")

    class Meta:
        model = Employee
        fields = ('username', 'position', 'email')


class SerializersProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'created_date_of_product')

    def validate_name(self, value):
        if len(value) > 25:
            raise serializers.ValidationError('The length of name product must be less 25 symbols')
        return value

    def validate_created_date_of_product(self, value):
        try:
            datetime.strptime(str(value), '%Y-%m-%d')
            return value
        except:
            raise serializers.ValidationError('Date format must be %Y-%m-%d')


class SerializersProviderAll(serializers.ModelSerializer):
    contacts = SerializersContact(many=True)
    products = SerializersProduct(many=True)
    employees = SerializersEmployee(many=True)

    class Meta:
        model = Provider
        fields = ('id', 'name', 'type', 'parent', 'date_created', 'employees',
                  'debt_to_provider', 'products', 'contacts', 'employees')


class SerializersProvider(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'name', 'type', 'parent', 'date_created', 'debt_to_provider')
        read_only_fields = ('debt_to_provider',)

    def validate_name(self, value):
        if len(value) > 50:
            raise serializers.ValidationError('The length of name objects must be less 50 symbols')
        return value
