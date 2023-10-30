from rest_framework import serializers
from .models import Provider, Product, Employee, Contact


class SerializersContact(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'email', 'country', 'city', 'street', 'building_number')


class SerializersEmployee(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'email', 'position', 'is_active')


class SerializersProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'created_date_of_product')

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.model = validated_data.get('model', instance.model)
        instance.created_date_of_product = validated_data.get('created_date_of_product',
                                                              instance.created_date_of_product)
        instance.save()
        return instance


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

    def create(self, validated_data):
        return Provider.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.parent = validated_data.get('parent', instance.parent)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.save()
        return instance
