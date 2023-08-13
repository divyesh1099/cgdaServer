from rest_framework import serializers
from .models import *

# Create your serializers here
class BillSummaryGemInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillSummaryGemInvoice
        fields = ['gemInvoiceNo']

class BillSummaryDataSerializer(serializers.ModelSerializer):
    gemInvoiceNos = BillSummaryGemInvoiceSerializer(many=True)
    
    class Meta:
        model = BillSummaryData
        fields = ['date', 'count', 'amount', 'gemInvoiceNos']

    def create(self, validated_data):
        gem_invoice_data = validated_data.pop('gemInvoiceNos')
        bill_summary_data = BillSummaryData.objects.create(**validated_data)
        
        gem_invoices = []
        for gem_invoice_item in gem_invoice_data:
            gem_invoice, created = BillSummaryGemInvoice.objects.get_or_create(**gem_invoice_item)
            gem_invoices.append(gem_invoice)
        
        bill_summary_data.gemInvoiceNos.set(gem_invoices)
        return bill_summary_data

class BillSummarySerializer(serializers.Serializer):
    status = serializers.CharField(max_length=10)
    iat = serializers.CharField(max_length=20)
    sub = serializers.CharField(max_length=20)
    aud = serializers.CharField(max_length=20)
    iss = serializers.CharField(max_length=20)
    data = BillSummaryDataSerializer(many=True)
    
    class Meta:
        model = BillSummary
        fields = ('__all__')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('id', None)
        return representation

    def create(self, validated_data):
        data = validated_data.pop('data')
        datas = []
        for individual_data in data:
            gem_invoice_nos = []
            gem_invoice_no_datas = individual_data.pop("gemInvoiceNos")
            for gem_invoice_no_data in gem_invoice_no_datas:
                old_gem_invoice_no_data, created = BillSummaryGemInvoice.objects.get_or_create(**gem_invoice_no_data)
                gem_invoice_nos.append(old_gem_invoice_no_data)
            old_bill_summary_data, created = BillSummaryData.objects.get_or_create(**individual_data)
            old_bill_summary_data.gemInvoiceNos.set(gem_invoice_nos)
            datas.append(old_bill_summary_data)
        bill_summary, created = BillSummary.objects.get_or_create(**validated_data)
        bill_summary.data.set(datas)
        return bill_summary