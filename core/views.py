from rest_framework import viewsets
from .models import Customer, Profession, Document, DataSheet
from .serializers import CustomerSerializer, ProfessionSerializer, \
    DocumentSerializer, DataSheetSerializer
from rest_framework.response import Response


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        active_customers = Customer.objects.filter(active=True)
        return active_customers

    def list(self, request, *args, **kwargs):
        # Can directly query objects here, method not needed.
        customers = self.get_queryset()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    # Function called when a specific object is requested through the endpoint.
    # Example: `/customers/3/` where 3 is the pk argument which will be used to retrieve the data.
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        customer = Customer.objects.create(
            name=data['name'], addr=data['addr'],
            data_sheet_id=data['data_sheet'],
        )
        
        profession = Profession.objects.get(id=data['profession'])
        customer.profession.add(profession)
        
        customer.save()
        
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer
