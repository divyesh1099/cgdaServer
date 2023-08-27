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

# class BillConsignProductsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BillConsignProducts
#         fields = '__all__'

# class BillConsignmentSerializer(serializers.ModelSerializer):
#     items = BillConsignProductsSerializer(many=True, read_only=True)

#     class Meta:
#         model = BillConsignment
#         fields = '__all__'

# class BillDetailsSerializer(serializers.ModelSerializer):
#     consignmentDetails = BillConsignmentSerializer(many=True, read_only=True)

#     class Meta:
#         model = BillDetails
#         fields = '__all__'

# class BillDeductionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BillDeductions
#         fields = '__all__'

class BillSerializer(serializers.Serializer):
    class Meta:
        model = BillDetailsData
        fields = ('__all__')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('id', None)
        return representation

    def create(self, validated_data):
        billDetailsDatas = validated_data.pop('')

# Updated Serializers
class BillDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetails
        fields = '__all__'

class BillDeductionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDeductions
        fields = '__all__'

class BillDeductionsAddlDtlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDeductionsAddlDtls
        fields = '__all__'

class BillingCycleDetailsSerializer(serializers.Serializer):
    unit = serializers.CharField(max_length=100, allow_blank=True)
    value = serializers.DecimalField(max_digits=15, decimal_places=2, default=0.00)

class BillConsignProductsSerializer(serializers.ModelSerializer):
    product_code = serializers.CharField(allow_blank=True, required=False)
    class Meta:
        model = BillConsignProducts
        fields = '__all__'

    def create(self, validated_data):
        billing_cycle_details_data = validated_data.pop('billing_cycle_details')
        instance = super().create(validated_data)
        instance.billing_cycle_details_unit = billing_cycle_details_data['unit']
        instance.billing_cycle_details_value = billing_cycle_details_data['value']
        instance.save()
        return instance

class BillConsignmentSerializer(serializers.ModelSerializer):
    consignment_details = BillConsignProductsSerializer(many=True)

    class Meta:
        model = BillConsignment
        fields = '__all__'

class DataItemSerializer(serializers.Serializer):
    sgst = serializers.FloatField()
    productBrand = serializers.CharField(max_length=100)
    suppliedQuantity = serializers.FloatField()
    freightSgst = serializers.FloatField()
    quantityOrdered = serializers.FloatField()
    igst = serializers.FloatField()
    productName = serializers.CharField(max_length=255)
    tdsUnderGst = serializers.CharField(max_length=20)
    quantityUnitType = serializers.CharField(max_length=100)
    unitPrice = serializers.FloatField()
    totalValue = serializers.FloatField()
    actualDeliveryDate = serializers.DateField()
    tdsUnderIncometax = serializers.CharField(max_length=20)
    hsnCode = serializers.CharField(max_length=20)
    freightCgst = serializers.FloatField()
    freightUtgst = serializers.FloatField()
    expectedDeliveryDate = serializers.DateField()
    cgst = serializers.FloatField()
    freightIgst = serializers.FloatField()
    cess = serializers.FloatField()
    freightCess = serializers.FloatField()
    utgst = serializers.FloatField()
    productCode = serializers.CharField(max_length=255)
    offering_type = serializers.CharField(max_length=50)
    acceptedQuantity = serializers.FloatField()
    frieghtCharge = serializers.FloatField()
    product_category_name = serializers.CharField(max_length=100)
    product_category_id = serializers.CharField(max_length=100)
    billing_cycle_details = serializers.DictField(child=serializers.CharField(), required=False)

class ConsignmentDetailsSerializer(serializers.Serializer):
    consigneeState = serializers.CharField(max_length=50)
    consigneeLastname = serializers.CharField(max_length=100)
    consigneeMobile = serializers.CharField(max_length=15)
    consigneeFname = serializers.CharField(max_length=100)
    items = BillConsignProductsSerializer(many=True)
    consigneeAddress = serializers.CharField(max_length=255)
    consigneePin = serializers.CharField(max_length=10)
    consigneeDistrict = serializers.CharField(max_length=80)

class DataSerializer(serializers.Serializer):
    pgMode = serializers.CharField(max_length=10)
    orderId = serializers.CharField(max_length=50)
    orderDate = serializers.DateField()
    orderAmount = serializers.DecimalField(max_digits=15, decimal_places=2)
    billNo = serializers.CharField(max_length=50)
    billDate = serializers.DateField()
    billAmount = serializers.DecimalField(max_digits=15, decimal_places=2)
    demandId = serializers.CharField(max_length=100)
    buyerOrg = serializers.CharField(max_length=255)
    buyerName = serializers.CharField(max_length=100)
    buyerEmail = serializers.CharField(max_length=100)
    buyerMobile = serializers.CharField(max_length=15)
    buyerAddress = serializers.CharField(max_length=255)
    buyerPincode = serializers.CharField(max_length=10)
    buyerDistrict = serializers.CharField(max_length=80)
    buyerState = serializers.CharField(max_length=50)
    buyerGstn = serializers.CharField(max_length=30, allow_blank=True, required=False)
    vendorName = serializers.CharField(max_length=255)
    vendorAddress = serializers.CharField(max_length=255)
    vendorCode = serializers.CharField(max_length=50)
    vendorDistrict = serializers.CharField(max_length=80)
    vendorState = serializers.CharField(max_length=50)
    vendorPin = serializers.CharField(max_length=10)
    vendorBankAccountNo = serializers.CharField(max_length=100)
    vendorBankIfscCode = serializers.CharField(max_length=15)
    vendorPan = serializers.CharField(max_length=12)
    vendorGstn = serializers.CharField(max_length=30, allow_blank=True, required=False)
    vendorUniqueId = serializers.CharField(max_length=10)
    vendorGstStatus = serializers.CharField(max_length=255, allow_blank=True, required=False)
    sellerId = serializers.CharField(max_length=255)
    supplyOrderNo = serializers.CharField(max_length=255)
    supplyOrderDate = serializers.DateField()
    designationFinancial = serializers.CharField(max_length=50)
    ifdConcurrance = serializers.CharField(max_length=1)
    ifdDiaryNo = serializers.CharField(max_length=50)
    ifdDiaryDate = serializers.DateField()
    consignmentDetails = ConsignmentDetailsSerializer(many=True)
    faFile = serializers.URLField()
    cracFile = serializers.URLField()
    contractFile = serializers.URLField()
    receiptNo = serializers.CharField(max_length=100)
    receiptDate = serializers.DateField()
    cracDate = serializers.DateField()
    billFile = serializers.URLField()
    invoiceFile = serializers.URLField()
    invoiceDate = serializers.DateField()
    invoiceNo = serializers.CharField(max_length=255)
    gemInvoiceNo = serializers.CharField(max_length=100)
    deductions = BillDeductionsSerializer(many=True, required=False)
    createOn = serializers.DateTimeField()
    transactionId = serializers.DecimalField(max_digits=40, decimal_places=0)

    def create(self, validated_data):
        consignment_data = validated_data.pop('bill_consignment', {})
        deductions_data = validated_data.pop('bill_deductions', {})

        bill_details = BillDetails.objects.create(**validated_data)

        consignment_serializer = BillConsignmentSerializer(data=consignment_data)
        if consignment_serializer.is_valid():
            consignment_serializer.save(gem_invoice_no=bill_details)

        deductions_serializer = BillDeductionsSerializer(data=deductions_data)
        if deductions_serializer.is_valid():
            deductions_serializer.save(gem_invoice_no=bill_details)

        return bill_details
class RootSerializer(serializers.Serializer):
    data = DataSerializer(many=True)

    def create(self, validated_data):
        billDetailsDatas = validated_data.pop('data')
        datas = []
        for billDetailsData in billDetailsDatas:
            bill_details_data, created = BillDetails.objects.get_or_create(**billDetailsData)
            datas.append(bill_details_data)
        bill_data, created = BillDetailsData.objects.get_or_create(**validated_data)
        bill_data.data.set(datas)
        return bill_data