# Generated by Django 4.0.3 on 2024-01-25 14:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crud', '0007_ventas'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ventas',
            new_name='registro_ventas',
        ),
    ]
