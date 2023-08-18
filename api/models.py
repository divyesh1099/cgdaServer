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
    sgst = models.DecimalField(max_digits=10, decimal_places=2)
    productBrand = models.CharField(max_length=100)
    suppliedQuantity = models.IntegerField()
    freightSgst = models.DecimalField(max_digits=10, decimal_places=2)
    quantityOrdered = models.IntegerField()
    igst = models.DecimalField(max_digits=10, decimal_places=2)
    productName = models.CharField(max_length=200)
    tdsUnderGst = models.CharField(max_length=10)
    quantityUnitType = models.CharField(max_length=50)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    totalValue = models.DecimalField(max_digits=10, decimal_places=2)
    actualDeliveryDate = models.DateField()
    tdsUnderIncometax = models.CharField(max_length=10)
    hsnCode = models.IntegerField()
    freightCgst = models.DecimalField(max_digits=10, decimal_places=2)
    freightUtgst = models.DecimalField(max_digits=10, decimal_places=2)
    expectedDeliveryDate = models.DateField()
    cgst = models.DecimalField(max_digits=10, decimal_places=2)
    freightIgst = models.DecimalField(max_digits=10, decimal_places=2)
    cess = models.DecimalField(max_digits=10, decimal_places=2)
    freightCess = models.DecimalField(max_digits=10, decimal_places=2)
    utgst = models.DecimalField(max_digits=10, decimal_places=2)
    productCode = models.CharField(max_length=100)
    offering_type = models.CharField(max_length=50)
    acceptedQuantity = models.IntegerField()
    frieghtCharge = models.DecimalField(max_digits=10, decimal_places=2)
    product_category_name = models.CharField(max_length=100)
    product_category_id = models.CharField(max_length=50)
    billing_cycle_details = models.ForeignKey(BillBillingCycleDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.productName
    
class BillConsignee(models.Model):
    consigneeState = models.CharField(max_length=100)
    consigneeLastname = models.CharField(max_length=200)
    consigneeMobile = models.CharField(max_length=15)
    consigneeFname = models.CharField(max_length=200)
    consigneeAddress = models.TextField(null=True, blank=True)
    consigneePin = models.CharField(max_length=10, null=True, blank=True)
    consigneeDistrict = models.CharField(max_length=100, null=True, blank=True)
    items = models.ManyToManyField(BillProduct, related_name='billConsignees')

    def __str__(self):
        return self.consigneeFname + ' ' + self.consigneeLastname
    
class BillOrder(models.Model):
    pgMode = models.CharField(max_length=100)
    orderId = models.CharField(max_length=100)
    orderDate = models.DateField()
    orderAmount = models.DecimalField(max_digits=10, decimal_places=2)
    billNo = models.CharField(max_length=100)
    billDate = models.DateField()
    billAmount = models.DecimalField(max_digits=10, decimal_places=2)
    demandId = models.CharField(max_length=100)
    buyerOrg = models.CharField(max_length=200)
    buyerName = models.CharField(max_length=200)
    buyerEmail = models.EmailField()
    buyerMobile = models.CharField(max_length=15)
    buyerAddress = models.TextField()
    buyerPincode = models.CharField(max_length=10)
    buyerDistrict = models.CharField(max_length=100)
    buyerState = models.CharField(max_length=100)
    buyerGstn = models.CharField(max_length=50, null=True, blank=True)
    vendorName = models.CharField(max_length=200)
    vendorAddress = models.TextField()
    vendorCode = models.CharField(max_length=100)
    vendorDistrict = models.CharField(max_length=100)
    vendorState = models.CharField(max_length=100)
    vendorPin = models.CharField(max_length=10)
    vendorBankAccountNo = models.CharField(max_length=100)
    vendorBankIfscCode = models.CharField(max_length=100)
    vendorPan = models.CharField(max_length=20)
    vendorGstn = models.CharField(max_length=50, null=True, blank=True)
    vendorUniqueId = models.CharField(max_length=50)
    vendorGstStatus = models.CharField(max_length=50, null=True, blank=True)
    sellerId = models.CharField(max_length=100)
    supplyOrderNo = models.CharField(max_length=100)
    supplyOrderDate = models.DateField()
    designationFinancial = models.CharField(max_length=10)
    ifdConcurrance = models.CharField(max_length=10)
    ifdDiaryNo = models.CharField(max_length=50)
    ifdDiaryDate = models.DateField()
    faFile = models.URLField()
    cracFile = models.URLField()
    contractFile = models.URLField()
    receiptNo = models.CharField(max_length=100)
    receiptDate = models.DateField()
    cracDate = models.DateField()
    billFile = models.URLField()
    invoiceFile = models.URLField()
    invoiceDate = models.DateField()
    invoiceNo = models.CharField(max_length=100)
    gemInvoiceNo = models.CharField(max_length=100)
    deductions = models.TextField(null=True, blank=True)
    createOn = models.DateTimeField()
    transactionId = models.CharField(max_length=100)
    consignmentDetails = models.ManyToManyField(BillConsignee, related_name='billOrders')

    def __str__(self):
        return self.orderId
    
class Bill(models.Model):
    data = models.ManyToManyField(BillOrder, related_name='bills')