"""
URL configuration for cgdaServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

# Creating Default Router
router = DefaultRouter()

# Register Viewsets with Router
router.register('bill', views.BillViewSet, basename='bill')
router.register('billProduct', views.BillProductViewSet, basename='billProduct')
router.register('billSummary', views.BillSummaryViewSet, basename='billSummary')
router.register('billConsignee', views.BillConsigneeViewSet, basename='billConsignee')
router.register('billSummaryData', views.BillSummaryDataViewSet, basename='billSummaryData')
router.register('billSummaryGemInvoice', views.BillSummaryGemInvoiceViewSet, basename='billSummaryGemInvoice')
router.register('billBillingCycleDetail', views.BillBillingCycleDetailViewSet, basename='billBillingCycleDetailViewSet')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
