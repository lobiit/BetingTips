# Generated by Django 3.2.7 on 2021-10-06 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_alter_customer_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=100, unique=True, verbose_name='Phone Number:2547XXXXXXXX'),
        ),
    ]