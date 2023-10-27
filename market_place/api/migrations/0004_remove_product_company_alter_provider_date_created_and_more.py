# Generated by Django 4.2.6 on 2023-10-27 08:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_provider_employees_alter_contact_company_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='company',
        ),
        migrations.AlterField(
            model_name='provider',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 27, 11, 46, 47, 857126), verbose_name='Время создания'),
        ),
        migrations.CreateModel(
            name='RelatedProviderToProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
                ('provider_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.provider')),
            ],
        ),
    ]