from django.db import models

# Create your models here.
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
    status = models.CharField(max_length=10)
    iat = models.CharField(max_length=20)
    sub = models.CharField(max_length=20)
    aud = models.CharField(max_length=20)
    iss = models.CharField(max_length=20)
    data = models.ManyToManyField(BillSummaryData, related_name='billSummaries')