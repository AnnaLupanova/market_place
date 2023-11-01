from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from datetime import datetime
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя пользователя', related_name='users')
    position = models.CharField('Должность', max_length=128)
    company = models.ForeignKey('Provider', on_delete=models.CASCADE, verbose_name='Сеть', related_name='employees')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотруники'

    def __str__(self):
        return f'{self.user.username}'


class Provider(MPTTModel):
    FACTORY = 'ЗАВОД'
    DISTRIBUTOR = 'ДИСТРИБЬЮТОР'
    DEALERSHIP = 'ДИЛЕРСКИЙ ЦЕНТР'
    RETAIL_CHAIN = 'КРУПНАЯ РОЗНИЧНАЯ СЕТЬ'
    INDIVIDUAL_ENTREPRENEUR = 'ИП'

    type_choices = [
        (FACTORY, 'Завод'),
        (DISTRIBUTOR, 'Дистрибьютор'),
        (DEALERSHIP, 'Дилерский центр'),
        (RETAIL_CHAIN, 'Крупная розничная сеть'),
        (INDIVIDUAL_ENTREPRENEUR, 'ИП')
    ]
    name = models.CharField('Название', max_length=128, unique=True)
    type = models.CharField('Тип сети', choices=type_choices, max_length=128)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='Поставщик')
    date_created = models.DateTimeField('Время создания', auto_now_add=True)
    debt_to_provider = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Задолженность')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    class MPTTMeta:
        order_insertion_by = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField('id', primary_key=True)
    name = models.CharField('Название', max_length=128)
    model = models.CharField('Модель', max_length=128)
    created_date_of_product = models.DateField('Дата выпуска')
    company = models.ManyToManyField('Provider',
                                     through="RelatedProviderToProduct", related_name='products')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Contact(models.Model):
    id = models.AutoField('id', primary_key=True)
    email = models.EmailField('email', max_length=128)
    country = models.CharField('Страна', max_length=128)
    city = models.CharField('Город', max_length=128)
    street = models.CharField('Улица', max_length=128)
    building_number = models.IntegerField('Номер дома')
    company = models.ForeignKey('Provider', on_delete=models.CASCADE, verbose_name='Сеть', related_name='contacts')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'{self.email}, {self.country},  {self.city}, {self.street}, {self.building_number}'


class RelatedProviderToProduct(models.Model):
    id = models.AutoField('id', primary_key=True)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    provider_id = models.ForeignKey('Provider', on_delete=models.CASCADE, verbose_name='Поставщик')

    class Meta:
        verbose_name = 'Продукт-Поставщик'
        verbose_name_plural = 'Продукты-Поставщики'

    def __str__(self):
        return f'{self.product_id} {self.provider_id}'
