from django.db import models

# Create your models here.
# ---------------------------------------------------------------------------------------------------------------------------------
# Bill Summary Models
# ---------------------------------------------------------------------------------------------------------------------------------
class BillSummaryGemInvoice(models.Model):
    gemInvoiceNo = models.CharField(max_length=20)

    def __str__(self):
        return self.gemInvoiceNo
    
class BillSummaryData(models.Model):
    date = models.DateField()
    count = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gemInvoiceNos = models.ManyToManyField(BillSummaryGemInvoice, related_name='billSummaryDatas')

    def __str__(self):
        return f"{self.date} - Count: {self.count}, Amount: {self.amount}"
    
class BillSummary(models.Model):
    data = models.ManyToManyField(BillSummaryData, related_name='billSummaries')

# ---------------------------------------------------------------------------------------------------------------------------------
# Bill Model Fields
# ---------------------------------------------------------------------------------------------------------------------------------
class BillBillingCycleDetail(models.Model):
    unit=models.CharField(max_length=50, null=True, blank=True)
    value=models.IntegerField(null=True, blank=True)

class BillProduct(models.Model):
    acceptedQuantity = models.IntegerField()
    actualDeliveryDate = models.DateField()
    cess = models.DecimalField(max_digits=10, decimal_places=2)
    cgst = models.DecimalField(max_digits=10, decimal_places=2)
    expectedDeliveryDate = models.DateField()
    frieghtCharge = models.DecimalField(max_digits=10, decimal_places=2)
    freightCess = models.DecimalField(max_digits=10, decimal_places=2)
    freightCgst = models.DecimalField(max_digits=10, decimal_places=2)
    freightIgst = models.DecimalField(max_digits=10, decimal_places=2)
    freightSgst = models.DecimalField(max_digits=10, decimal_places=2)
    freightUtgst = models.DecimalField(max_digits=10, decimal_places=2)
    hsnCode = models.IntegerField()
    igst = models.DecimalField(max_digits=10, decimal_places=2)
    offering_type = models.CharField(max_length=50)
    productBrand = models.CharField(max_length=100)
    productCode = models.CharField(max_length=100)
    product_category_id = models.CharField(max_length=50)
    product_category_name = models.CharField(max_length=100)
    productName = models.CharField(max_length=200)
    quantityOrdered = models.IntegerField()
    quantityUnitType = models.CharField(max_length=50)
    sgst = models.DecimalField(max_digits=10, decimal_places=2)
    suppliedQuantity = models.IntegerField()
    tdsUnderGst = models.CharField(max_length=10)
    tdsUnderIncometax = models.CharField(max_length=10)
    totalValue = models.DecimalField(max_digits=10, decimal_places=2)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    utgst = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle_details = models.ForeignKey(BillBillingCycleDetail, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.productName
    
class BillConsignee(models.Model):
    consigneeAddress = models.TextField(null=True, blank=True)
    consigneeDistrict = models.CharField(max_length=100, null=True, blank=True)
    consigneeFname = models.CharField(max_length=200)
    consigneeLastname = models.CharField(max_length=200)
    consigneeMobile = models.CharField(max_length=15)
    consigneePin = models.CharField(max_length=10, null=True, blank=True)
    consigneeState = models.CharField(max_length=100)
    items = models.ManyToManyField(BillProduct, related_name='billConsignees')

    def __str__(self):
        return self.consigneeFname + ' ' + self.consigneeLastname
    
class BillOrder(models.Model):
    billAmount = models.DecimalField(max_digits=10, decimal_places=2)
    billDate = models.DateField()
    billFile = models.URLField()
    billNo = models.CharField(max_length=100)
    buyerAddress = models.TextField()
    buyerDistrict = models.CharField(max_length=100)
    buyerEmail = models.EmailField()
    buyerGstn = models.CharField(max_length=50, null=True, blank=True)
    buyerMobile = models.CharField(max_length=15)
    buyerName = models.CharField(max_length=200)
    buyerOrg = models.CharField(max_length=200)
    buyerPincode = models.CharField(max_length=10)
    buyerState = models.CharField(max_length=100)
    contractFile = models.URLField()
    createOn = models.DateTimeField()
    cracDate = models.DateField()
    cracFile = models.URLField()
    deductions = models.TextField(null=True, blank=True)
    demandId = models.CharField(max_length=100)
    designationFinancial = models.CharField(max_length=10)
    faFile = models.URLField()
    gemInvoiceNo = models.CharField(max_length=100)
    ifdConcurrance = models.CharField(max_length=10)
    ifdDiaryDate = models.DateField()
    ifdDiaryNo = models.CharField(max_length=50)
    invoiceDate = models.DateField()
    invoiceFile = models.URLField()
    invoiceNo = models.CharField(max_length=100)
    orderId = models.CharField(max_length=100)
    orderAmount = models.DecimalField(max_digits=10, decimal_places=2)
    orderDate = models.DateField()
    pgMode = models.CharField(max_length=100)
    receiptDate = models.DateField()
    receiptNo = models.CharField(max_length=100)
    sellerId = models.CharField(max_length=100)
    supplyOrderDate = models.DateField()
    supplyOrderNo = models.CharField(max_length=100)
    transactionId = models.CharField(max_length=100)
    vendorAddress = models.TextField()
    vendorBankAccountNo = models.CharField(max_length=100)
    vendorBankIfscCode = models.CharField(max_length=100)
    vendorCode = models.CharField(max_length=100)
    vendorDistrict = models.CharField(max_length=100)
    vendorGstStatus = models.CharField(max_length=50, null=True, blank=True)
    vendorGstn = models.CharField(max_length=50, null=True, blank=True)
    vendorName = models.CharField(max_length=200)
    vendorPan = models.CharField(max_length=20)
    vendorPin = models.CharField(max_length=10)
    vendorState = models.CharField(max_length=100)
    vendorUniqueId = models.CharField(max_length=50)
    consignmentDetails = models.ManyToManyField(BillConsignee, related_name='billOrders')

    def __str__(self):
        return self.orderId
    
class Bill(models.Model):
    data = models.ManyToManyField(BillOrder, related_name='bills')

# ---------------------------------------------------------------------------------------------------------------------------------
# Actual Tables
# ---------------------------------------------------------------------------------------------------------------------------------

class BillDetails(models.Model):
    billAmount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    billDate = models.DateTimeField(null=True)
    billFile = models.CharField(max_length=255, null=True)
    billNo = models.CharField(max_length=50, null=True)
    buyerAddress = models.CharField(max_length=255, null=True)
    buyerDistrict = models.CharField(max_length=80, null=True)
    buyerEmail = models.CharField(max_length=100, null=True)
    buyerGstn = models.CharField(max_length=30, null=True, blank=True)
    buyerMobile = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    buyerName = models.CharField(max_length=100, null=True)
    buyerOrg = models.CharField(max_length=255, null=True)
    buyerPincode = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    buyerState = models.CharField(max_length=50, null=True)
    contractFile = models.CharField(max_length=255, null=True)
    cracDate = models.DateTimeField(null=True)
    cracFile = models.CharField(max_length=255, null=True)
    createdDatetime = models.DateTimeField(null=True)
    createOn = models.DateTimeField(null=True)
    demandId = models.CharField(max_length=100, null=True)
    designationFinancial = models.CharField(max_length=50, null=True)
    faFile = models.CharField(max_length=255, null=True)
    gemInvoiceNo = models.CharField(max_length=100, primary_key=True)
    ifdConcurrance = models.IntegerField(null=True)
    ifdDiaryDate = models.DateTimeField(null=True)
    ifdDiaryNo = models.CharField(max_length=50, null=True)
    invoiceDate = models.DateTimeField(null=True)
    invoiceFile = models.CharField(max_length=255, null=True)
    invoiceNo = models.CharField(max_length=255, null=True)
    orderAmount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    orderDate = models.DateTimeField()
    orderId = models.CharField(max_length=255)
    pgMode = models.CharField(max_length=10, null=True)
    receiptDate = models.DateTimeField(null=True)
    receiptNo = models.CharField(max_length=100, null=True)
    requestSer = models.IntegerField()
    responseSer = models.IntegerField(null=True)
    sellerId = models.CharField(max_length=255, null=True)
    syncDatetime = models.DateTimeField(null=True)
    supplyOrderDate = models.DateTimeField(null=True)
    supplyOrderNo = models.CharField(max_length=255, null=True)
    transactionId = models.DecimalField(max_digits=40, decimal_places=0, null=True)
    vendorAddress = models.CharField(max_length=255, null=True)
    vendorBankAccountNo = models.CharField(max_length=100, null=True)
    vendorBankIfscCode = models.CharField(max_length=15, null=True)
    vendorCode = models.CharField(max_length=50, null=True)
    vendorDistrict = models.CharField(max_length=80, null=True)
    vendorGstStatus = models.CharField(max_length=255, null=True, blank=True)
    vendorGstn = models.CharField(max_length=30, null=True, blank=True)
    vendorName = models.CharField(max_length=255, null=True)
    vendorPan = models.CharField(max_length=12, null=True)
    vendorPin = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    vendorState = models.CharField(max_length=50, null=True)
    vendorUniqueId = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'bill_details'

class BillConsignment(models.Model):
    consigneeAddress = models.CharField(max_length=255, null=True)
    consigneeDistrict = models.CharField(max_length=80, null=True)
    consigneeFname = models.CharField(max_length=100, null=True)
    consigneeLastname = models.CharField(max_length=100, null=True)
    consigneeMobile = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    consigneePin = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    consigneeState = models.CharField(max_length=50, null=True)
    consignmentSer = models.AutoField(primary_key=True)
    gemInvoiceNo = models.OneToOneField(BillDetails, on_delete=models.CASCADE)
    def __str__(self):
        return self.gem_invoice_no

    class Meta:
        db_table = 'gemilms.bill_consignment'

class BillDeductions(models.Model):
    dednAmount = models.FloatField(null=True)
    dednName = models.CharField(max_length=150, null=True)
    dednReason = models.TextField(null=True)
    dednType = models.CharField(max_length=150, null=True)
    deductionSerialNo = models.AutoField(primary_key=True)
    gemInvoiceNo = models.ForeignKey(BillDetails, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'bill_deductions'

class BillDeductionsAddlDtls(models.Model):
    deductionSerialNo = models.ForeignKey(BillDeductions, on_delete=models.CASCADE)
    additionalDetailsSerialNo = models.AutoField(primary_key=True)
    ldDays = models.IntegerField()
    class Meta:
        db_table = 'bill_deductions_addl_dtls'

class BillConsignProducts(models.Model):
    acceptedQuantity = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    actualDeliveryDate = models.DateTimeField(null=True)
    billingCycleDetailsUnit = models.CharField(max_length=20, null=True, blank=True) # Remember to extract this from the billing_cycle_details key's "unit" key's value
    billingCycleDetailsValue = models.IntegerField(null=True, blank=True) # Remember to extract this from the billing_cycle_details key's "value" key's value
    cess = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    consignmentSer = models.ManyToManyField(BillConsignment, related_name='billConsignmentProducts', blank=True, null=True)
    expectedDeliveryDate = models.DateTimeField(null=True)
    frieghtCharge = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    freightCess = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    freightCgst = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    freightIgst = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    freightSgst = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    freightUtgst = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    hsnCode = models.CharField(max_length=20, null=True)
    igst = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    offeringType = models.CharField(max_length=50, null=True)
    productBrand = models.CharField(max_length=100, null=True)
    productCategoryId = models.CharField(max_length=100, null=True)
    productCategoryName = models.CharField(max_length=100, null=True)
    productCode = models.CharField(max_length=1000, null=True)
    productName = models.CharField(max_length=255, null=True)
    productSerialNo = models.AutoField(primary_key=True)
    quantityOrdered = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    quantityUnitType = models.CharField(max_length=100, null=True)
    sgst = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    suppliedQuantity = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    tdsUnderGst = models.CharField(max_length=20, null=True)
    tdsUnderIncomeTax = models.CharField(max_length=20, null=True)
    totalValue = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    unitPrice = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    utgst = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    def __str__(self):
        return self.productCode
    
    class Meta:
        db_table = 'bill_consign_products'

class BillDetailsData(models.Model):
    data = models.ManyToManyField(BillDetails, related_name="billDetailsDatas")