from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your serializers here
# ---------------------------------------------------------------------------------------------------------------------------------
# Bill Summary Serializers Fields
# ---------------------------------------------------------------------------------------------------------------------------------
class CustomizedTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Customized Response, removing the Refresh Token
        if data["refresh"]:
            data.pop("refresh")
        if data["access"]:
            token = data["access"]
            data["token"] = token
            data.pop("access")
        return data

# ---------------------------------------------------------------------------------------------------------------------------------
# Bill Summary Serializers Fields
# ---------------------------------------------------------------------------------------------------------------------------------
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
        bill_summary_data, created = BillSummaryData.objects.get_or_create(**validated_data)
        
        gem_invoices = []
        for gem_invoice_item in gem_invoice_data:
            gem_invoice, created = BillSummaryGemInvoice.objects.get_or_create(**gem_invoice_item)
            gem_invoices.append(gem_invoice)
        
        bill_summary_data.gemInvoiceNos.set(gem_invoices)
        return bill_summary_data

class BillSummarySerializer(serializers.Serializer):
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
    
# ---------------------------------------------------------------------------------------------------------------------------------
# Bill Summary Serializers
# ---------------------------------------------------------------------------------------------------------------------------------
class BillBillingCycleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillBillingCycleDetail
        fields = ['unit', 'value']

class BillProductSerializer(serializers.ModelSerializer):
    billing_cycle_details = BillBillingCycleDetailSerializer()
    class Meta:
        model = BillProduct
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('id', None)
        return representation

    def create(self, validated_data):
        billing_cycle_details_data = validated_data.pop('billing_cycle_details')
        billing_cycle_detail, created = BillBillingCycleDetail.objects.get_or_create(**billing_cycle_details_data)
        validated_data['billing_cycle_details'] = billing_cycle_detail  
        item, created = BillProduct.objects.get_or_create(**validated_data)
        return item
    
class BillConsigneeSerializer(serializers.Serializer):
    consigneeState = serializers.CharField()
    consigneeLastname = serializers.CharField()
    consigneeMobile = serializers.CharField()
    consigneeFname = serializers.CharField()
    consigneeAddress = serializers.CharField()
    consigneePin = serializers.CharField()
    consigneeDistrict = serializers.CharField()
    items = BillProductSerializer(many=True)
    class Meta:
        model = BillConsignee
        fields = ('__all__')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('id', None)
        return representation

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        items = []
        for item in items_data:
            billing_cycle_detail_data = item.pop('billing_cycle_details')
            billing_cycle_detail, created = BillBillingCycleDetail.objects.get_or_create(**billing_cycle_detail_data)
            item["billing_cycle_details"]=billing_cycle_detail
            product, created = BillProduct.objects.get_or_create(**item)
            items.append(product)
        consignee_data, created = BillConsignee.objects.get_or_create(**validated_data)
        consignee_data.items.set(items)
        return consignee_data
        
class BillOrderSerializer(serializers.Serializer):
    pgMode = serializers.CharField()
    orderId = serializers.CharField()
    orderDate = serializers.DateField()
    orderAmount = serializers.DecimalField(max_digits=10, decimal_places=2)
    billNo = serializers.CharField()
    billDate = serializers.DateField()
    billAmount = serializers.DecimalField(max_digits=10, decimal_places=2)
    demandId = serializers.CharField()
    buyerOrg = serializers.CharField()
    buyerName = serializers.CharField()
    buyerEmail = serializers.EmailField()
    buyerMobile = serializers.CharField()
    buyerAddress = serializers.CharField()
    buyerPincode = serializers.CharField()
    buyerDistrict = serializers.CharField()
    buyerState = serializers.CharField()
    buyerGstn = serializers.CharField(allow_blank=True)
    vendorName = serializers.CharField()
    vendorAddress = serializers.CharField()
    vendorCode = serializers.CharField()
    vendorDistrict = serializers.CharField()
    vendorState = serializers.CharField()
    vendorPin = serializers.CharField()
    vendorBankAccountNo = serializers.CharField()
    vendorBankIfscCode = serializers.CharField()
    vendorPan = serializers.CharField()
    vendorGstn = serializers.CharField(allow_blank=True)
    vendorUniqueId = serializers.CharField()
    vendorGstStatus = serializers.CharField(allow_blank=True)
    sellerId = serializers.CharField()
    supplyOrderNo = serializers.CharField()
    supplyOrderDate = serializers.DateField()
    designationFinancial = serializers.CharField()
    ifdConcurrance = serializers.CharField()
    ifdDiaryNo = serializers.CharField()
    ifdDiaryDate = serializers.DateField()
    faFile = serializers.URLField()
    cracFile = serializers.URLField()
    contractFile = serializers.URLField()
    receiptNo = serializers.CharField()
    receiptDate = serializers.DateField()
    cracDate = serializers.DateField()
    billFile = serializers.URLField()
    invoiceFile = serializers.URLField()
    invoiceDate = serializers.DateField()
    invoiceNo = serializers.CharField()
    gemInvoiceNo = serializers.CharField()
    deductions = serializers.CharField(allow_blank=True)
    createOn = serializers.DateTimeField()
    transactionId = serializers.CharField()
    consignmentDetails = BillConsigneeSerializer(many=True)

    class Meta:
        model = BillOrder
        fields = ('__all__')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('id', None)
        return representation
    
    def create(self, validated_data):
        consignee_data = validated_data.pop('consignmentDetails')
        consignment_details = []
        for consignee in consignee_data:
            items_data = consignee.pop('items')
            items = []
            for item in items_data:
                billing_cycle_detail_data = item.pop('billing_cycle_details')
                billing_cycle_detail, created = BillBillingCycleDetail.objects.get_or_create(**billing_cycle_detail_data)
                item["billing_cycle_details"]=billing_cycle_detail
                product, created = BillProduct.objects.get_or_create(**item)
                items.append(product)
            consignee_data, created = BillConsignee.objects.get_or_create(**consignee)
            consignee_data.items.set(items)
            consignment_details.append(consignee_data)
        order_data, created = BillOrder.objects.get_or_create(**validated_data)
        order_data.consignmentDetails.set(consignment_details)
        return order_data
    
class BillSerializer(serializers.Serializer):
    data = BillOrderSerializer(many=True)
    
    class Meta:
        model = Bill
        fields = ('__all__')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('id', None)
        return representation

    def create(self, validated_data):
        order_data = validated_data.pop('data')
        datas = []
        for order in order_data:
            consignee_data = order.pop('consignmentDetails')
            consignment_details = []
            for consignee in consignee_data:
                items_data = consignee.pop('items')
                items = []
                for item in items_data:
                    billing_cycle_detail_data = item.pop('billing_cycle_details')
                    billing_cycle_detail, created = BillBillingCycleDetail.objects.get_or_create(**billing_cycle_detail_data)
                    item["billing_cycle_details"]=billing_cycle_detail
                    product, created = BillProduct.objects.get_or_create(**item)
                    items.append(product)
                consignee_data, created = BillConsignee.objects.get_or_create(**consignee)
                consignee_data.items.set(items)
                consignment_details.append(consignee_data)
            order_data, created = BillOrder.objects.get_or_create(**order)
            order_data.consignmentDetails.set(consignment_details)
            datas.append(order_data)
        bill_data, created = Bill.objects.get_or_create(**validated_data)
        bill_data.data.set(datas)
        return bill_data