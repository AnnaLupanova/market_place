# Generated by Django 4.2.6 on 2023-10-27 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_relatedprovidertoproduct_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ManyToManyField(related_name='products', through='api.RelatedProviderToProduct', to='api.provider'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='relatedprovidertoproduct',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='relatedprovidertoproduct',
            name='provider_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.provider', verbose_name='Поставщик'),
        ),
    ]