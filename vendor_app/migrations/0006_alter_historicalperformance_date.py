# Generated by Django 5.0.4 on 2024-05-05 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_app', '0005_purchaseorder_delivered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformance',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
