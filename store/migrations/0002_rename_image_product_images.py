# Generated by Django 5.1.7 on 2025-03-21 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image',
            new_name='images',
        ),
    ]
