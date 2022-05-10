from rest_framework import viewsets, status
from .models import Customer, Profession, Document, DataSheet
from .serializers import CustomerSerializer, ProfessionSerializer, \
    DocumentSerializer, DataSheetSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, # Locally enable DFB for current viewset.
                       SearchFilter,]
    filterset_fields = ['name',]
    # data_sheet__description is searching in a foreign relation data_sheet in the description field.
    search_fields = ['name', 'addr', 'data_sheet__description',]

    def get_queryset(self):
        addr = self.request.query_params.get('addr')
        status = False if self.request.query_params.get('status') == 'False' else True
        if addr:
            customers = Customer.objects.filter(addr__contains=addr, active=status)
        else:
            customers = Customer.objects.all().order_by('-active')
        return customers

    # If we want to use DjangoFilterBackend by defining filterset_fields,
    # list cannot be overriden or we'll have to add DjangoFilterBackend code in list method.
    # def list(self, request, *args, **kwargs):
    #     # Can directly query objects here, method not needed.
    #     customers = self.get_queryset()
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)

    # Function called when a specific object is requested through the endpoint.
    # Example: `/customers/3/` where 3 is the pk argument which will be used to retrieve the data.
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)

    # Postman parameters must be passed through the body section. 
    # They are not received through params, header or other section.
    # request.data will be empty in this case.
    def create(self, request, *args, **kwargs):
        data = request.data

        customer = Customer.objects.create(
            name=data['name'],
            addr=data['addr'],
            data_sheet_id=data['data_sheet'],
        )

        profession = Profession.objects.get(id=data['profession'])
        customer.profession.add(profession)

        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        # change the value only when a new value parameter is passed for that object
        customer.name = request.data.get('name', customer.name)
        customer.addr = request.data.get('addr', customer.addr)
        customer.data_sheet_id = request.data.get(
            'data_sheet', customer.data_sheet_id)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # By default, all object will run the method.
    # When detail=True, only that specific object `customers/3/deactivate` will run it.
    @action(detail=True)
    def deactivate(self, request, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=True)
    def activate(self, request, **kwargs):
        customer = self.get_object()
        customer.active = True
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
