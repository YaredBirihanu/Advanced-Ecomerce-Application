# Generated by Django 5.1.7 on 2025-04-04 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_orderproduct_variation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='product_price',
            field=models.FloatField(default=0),
        ),
    ]
