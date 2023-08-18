from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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