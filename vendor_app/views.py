from django.shortcuts import render
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Sum, Count, F, ExpressionWrapper, DurationField
from datetime import timedelta

# Create your views here.

class VendorListCreateApi(generics.ListCreateAPIView):
    serializer_class = VendorSerializer

    def get_queryset(self):
        queryset = Vendor.objects.all()
        return queryset

    def create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,
                                         many=True)
        return Response(serializer.data)
    

class VendorRetrieveUpdateDestoryApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VendorSerializer

    def get_queryset(self):
        queryset = Vendor.objects.all()
        return queryset
    
    def get(self, request, pk):
        object = self.get_object()
        serializer = self.get_serializer(object)
        return Response(serializer.data)
    
    def put(self, request, pk):
        object = self.get_object()
        data = request.data
        serializer = self.get_serializer(object, data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        object = self.get_object()
        object.delete()
        return Response("Vendor Deleted Successfully!")
    

class PurchaseOrderListCreateApi(generics.ListCreateAPIView):
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        return queryset

    def create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,
                                         many=True)
        return Response(serializer.data)
    

class PurchaseOrderRetrieveUpdateDestoryApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        return queryset
    
    def get(self, request, pk):
        object = self.get_object()
        serializer = self.get_serializer(object)
        return Response(serializer.data)
    
    def put(self, request, pk):
        object = self.get_object()
        data = request.data
        serializer = self.get_serializer(object, data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        object = self.get_object()
        object.delete()
        return Response("Purchase Order Deleted Successfully!")
    
class PurchaseOrderAcknowledgeUpdateApi(generics.CreateAPIView):
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        return queryset
    
    def create(self, request, pk):
        object = self.get_object()
        old_data = self.get_serializer(object).data
        data = request.data
        old_data['acknowledgment_date'] = data['acknowledgment_date']
        data = request.data
        serializer = self.get_serializer(object, old_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        date_difference = ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=DurationField()
                    )
        agr = PurchaseOrder.objects.filter(acknowledgment_date__isnull=False).aggregate(
            response=Sum(date_difference),count=Count('id') 
        )
        history, _ = HistoricalPerformance.objects.get_or_create(
            vendor=object.vendor
        )
        history.average_response_time=agr['response'].days
        history.save(update_fields=['average_response_time'])
        return Response(serializer.data)
    
class HistoryListApi(generics.ListAPIView):
    serializer_class = HistoricalPerformanceSerializer
    
    def get(self, request, vendor_id):
        try:
            queryset = HistoricalPerformance.objects.get(vendor=vendor_id)
            serializer = self.get_serializer(queryset)
            data = serializer.data
        except Exception as e:
            data = "No update of completed PO for this Vendor"
        return Response(data)
    
