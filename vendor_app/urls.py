from django.urls import path
from . import views

urlpatterns = [
    path('vendors/', views.VendorListCreateApi.as_view()),
    path('vendors/<int:pk>/', views.VendorRetrieveUpdateDestoryApi.as_view()),
    path('purchase_orders/', views.PurchaseOrderListCreateApi.as_view()),
    path('purchase_orders/<int:pk>/', views.PurchaseOrderRetrieveUpdateDestoryApi.as_view()),
    path('purchase_orders/<int:pk>/acknowledge/', views.PurchaseOrderAcknowledgeUpdateApi.as_view()),
    path('vendors/<int:vendor_id>/performance/', views.HistoryListApi.as_view()),
    path('vendors/<int:vendor_id>/performance/', views.HistoryListApi.as_view()),


]