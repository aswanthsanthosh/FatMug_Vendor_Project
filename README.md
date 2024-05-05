# FatMug_Vendor_Project

In this Project I have used SQlite as the Database and a Base database file has been pushed with the Code which I was used for Testing
virtual environment myvenv has been added and all needed dependencies is added in that environment
API End Point used in this Projects are :-
 -  /api/vendors/ - for vendor POST and GET
 -  /api/vendors/<int:pk>/ - for Retreive, Update and Delete Vendor
 -  /api/purchase_orders/ - for Purchase Order POST and GET
 - /api/purchase_orders/<int:pk>/ - for Retreive, Update and Delete Purchase Order
 - /api/purchase_orders/<int:pk>/acknowledge/ - POST method used for patching the acknowledgment date; this is used only to update the acknowledge date
 - /api/vendors/<int:vendor_id>/performance/ - used for tracking of vendor performance api
