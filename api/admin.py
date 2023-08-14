from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BillSummaryGemInvoice)
admin.site.register(BillSummaryData)
admin.site.register(BillSummary)

admin.site.register(BillBillingCycleDetail)
admin.site.register(BillProduct)
admin.site.register(BillConsignee)
admin.site.register(BillOrder)
admin.site.register(Bill)