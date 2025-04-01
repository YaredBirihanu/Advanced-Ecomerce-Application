# Generated by Django 5.1.7 on 2025-04-01 08:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_full_name_remove_order_phone_number_and_more'),
        ('store', '0004_alter_variation_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='amonunt_paid',
            new_name='amount_paid',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='variation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(max_length=100),
        ),
    ]
