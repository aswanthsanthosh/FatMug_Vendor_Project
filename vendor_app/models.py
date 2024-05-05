from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F,Q,Sum, Count

# Create your models here.

StatusChoices = (('pending', 'pending'),
                 ('completed', 'completed'),
                 ('canceled', 'canceled'))

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=10)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=10,  unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField()
    delivered_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20,choices=StatusChoices, default='pending')
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField(auto_now=True)
    acknowledgment_date = models.DateTimeField(null=True)

@receiver(post_save, sender=PurchaseOrder)  # Decorator to connect the function to the post_save signal
def po_post_save(sender, instance, created, **kwargs):
    print(instance.status)
    if instance.status == 'completed':
        history, _ = HistoricalPerformance.objects.get_or_create(
            vendor=instance.vendor
        )
        On_aggregates = PurchaseOrder.objects.filter(vendor=instance.vendor, delivery_date__lte=F('delivered_date') ).aggregate(
                            count=Count('id'))
        Total_aggregates = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').aggregate(
                    quality_rating=Sum('quality_rating')/Count('id'), count=Count('id')
        )
        aggregate = PurchaseOrder.objects.filter(vendor=instance.vendor).aggregate(
            count=Count('id')
        )
        history.on_time_delivery_rate = On_aggregates['count']/Total_aggregates['count']
        history.quality_rating_avg = Total_aggregates['quality_rating']
        history.fulfillment_rate = Total_aggregates['count']/aggregate['count']
        history.save(update_fields=['on_time_delivery_rate', 'quality_rating_avg', 'fulfillment_rate'])


                
                




