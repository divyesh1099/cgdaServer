from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics

# Create your views here.
class CustomizedTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomizedTokenObtainPairSerializer

class BillSummaryGemInvoiceViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = BillSummaryGemInvoice.objects.all()
    serializer_class=BillSummaryGemInvoiceSerializer

class BillSummaryDataViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = BillSummaryData.objects.all()
    serializer_class=BillSummaryDataSerializer

class BillSummaryViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = BillSummary.objects.all()
    serializer_class=BillSummarySerializer

class BillBillingCycleDetailViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = BillBillingCycleDetail.objects.all()
    serializer_class=BillBillingCycleDetailSerializer

class BillProductViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = BillProduct.objects.all()
    serializer_class=BillProductSerializer

class BillConsigneeViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = BillConsignee.objects.all()
    serializer_class=BillConsigneeSerializer

class BillOrderViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = BillOrder.objects.all()
    serializer_class = BillOrderSerializer

class BillViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Bill.objects.all()
    serializer_class=BillSerializer

class BillDetailsViewSet(viewsets.ModelViewSet):
    queryset = BillDetails.objects.all()
    serializer_class = BillDetailsSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.get('data')
        for bill_data in data:
            consignment_data = bill_data.pop('consignmentDetails')
            deductions_data = bill_data.pop('deductions')
            
            consignment_items = consignment_data[0].pop('items')
            
            # Create BillDetails instance
            bill_details_serializer = self.get_serializer(data=bill_data)
            bill_details_serializer.is_valid(raise_exception=True)
            bill_details = bill_details_serializer.save()
            
            # Create BillConsignment instance
            consignment_data[0]['consignment_ser'] = bill_details.id
            consignment_serializer = BillConsignmentSerializer(data=consignment_data[0])
            consignment_serializer.is_valid(raise_exception=True)
            consignment = consignment_serializer.save()
            
            # Create BillConsignProducts instances
            for item_data in consignment_items:
                item_data['consignment_ser'] = consignment.id
                consign_products_serializer = BillConsignProductsSerializer(data=item_data)
                consign_products_serializer.is_valid(raise_exception=True)
                consign_products_serializer.save()
            
            # Create BillDeductions instance
            if deductions_data: 
                deductions_data['gem_invoice_no'] = bill_details.gem_invoice_no
                deductions_serializer = BillDeductionsSerializer(data=deductions_data)
                deductions_serializer.is_valid(raise_exception=True)
                deductions_serializer.save()

        return Response({'message': 'Data saved into target models successfully'}, status=status.HTTP_201_CREATED)

# Updated Views
class BillDetailsListView(viewsets.ModelViewSet):
    queryset = BillDetails.objects.all()
    serializer_class = BillDetailsSerializer

class BillConsignmentListView(viewsets.ModelViewSet):
    queryset = BillConsignment.objects.all()
    serializer_class = BillConsignmentSerializer

class BillConsignProductsListView(viewsets.ModelViewSet):
    queryset = BillConsignProducts.objects.all()
    serializer_class = BillConsignProductsSerializer

class BillDeductionsListView(viewsets.ModelViewSet):
    queryset = BillDeductions.objects.all()
    serializer_class = BillDeductionsSerializer

class BillDeductionsAddlDtlsListView(viewsets.ModelViewSet):
    queryset = BillDeductionsAddlDtls.objects.all()
    serializer_class = BillDeductionsAddlDtlsSerializer

class JSONDataView(viewsets.ModelViewSet):
    queryset = BillDetailsData.objects.all()
    serializer_class = RootSerializer
    def post(self, request):
        data = request.data.get('data', [])
        serializer = RootSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Data saved into target models successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)