from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'created_date_of_product',)


@admin.action(description='Обнулить задолженность перед поставщиком')
def reset_debt(modeladmin, request, queryset):
    queryset.update(debt_to_provider=0.0)


class ProviderInline(admin.TabularInline):
    model = Provider
    extra = 1


@admin.register(Provider)
class ProviderAdmin(MPTTModelAdmin):
    actions = [reset_debt]
    inlines = [ProviderInline]
    list_display = ('name', 'type', 'parent', 'date_created',  'debt_to_provider',)
    list_filter = ['contacts__city']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'company', 'country', 'city', 'street', 'building_number')
    list_filter = ['city']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'position', 'company')


@admin.register(RelatedProviderToProduct)
class RelatedProviderToProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_id', 'provider_id')