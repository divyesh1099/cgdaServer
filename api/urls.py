from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *
urlpatterns = [
    path('token/', CustomizedTokenObtainPairView.as_view(), name='token_obtain_pair'),
]