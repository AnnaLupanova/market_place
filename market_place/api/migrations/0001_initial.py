# Generated by Django 4.2.6 on 2023-10-27 06:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название')),
                ('type', models.CharField(choices=[('Завод', 'Завод'), ('Дистрибьютор', 'Дистрибьютор'), ('Дилерский центр', 'Дилерский центр'), ('Крупная розничная сеть', 'Крупная розничная сеть'), ('ИП', 'ИП')], max_length=128, verbose_name='Тип сети')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2023, 10, 27, 9, 50, 7, 170208), verbose_name='Время создания')),
                ('employees', models.IntegerField(verbose_name='Сотрудники')),
                ('debt_to_provider', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Задолженность')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='api.provider', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('model', models.CharField(max_length=128, verbose_name='Модель')),
                ('created_date_of_product', models.DateField(verbose_name='created_date')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.provider', verbose_name='Сеть')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('first_name', models.CharField(max_length=128, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=128, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=128, verbose_name='email')),
                ('position', models.CharField(max_length=128, verbose_name='Должность')),
                ('is_active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='api.provider', verbose_name='Сеть')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотруники',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('email', models.EmailField(max_length=128, verbose_name='email')),
                ('country', models.CharField(max_length=128, verbose_name='Страна')),
                ('city', models.CharField(max_length=128, verbose_name='Город')),
                ('street', models.CharField(max_length=128, verbose_name='Улица')),
                ('building_number', models.IntegerField(verbose_name='Номер дома')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to='api.provider', verbose_name='Сеть')),
            ],
            options={
                'verbose_name': 'Контакт',
                'verbose_name_plural': 'Контакты',
            },
        ),
    ]
