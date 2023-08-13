from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets

# Create your views here.
class BillSummaryGemInvoiceViewSet(viewsets.ModelViewSet):
    queryset = BillSummaryGemInvoice.objects.all()
    serializer_class=BillSummaryGemInvoiceSerializer

class BillSummaryDataViewSet(viewsets.ModelViewSet):
    queryset = BillSummaryData.objects.all()
    serializer_class=BillSummaryDataSerializer

class BillSummaryViewSet(viewsets.ModelViewSet):
    queryset = BillSummary.objects.all()
    serializer_class=BillSummarySerializer