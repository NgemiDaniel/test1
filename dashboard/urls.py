from django.urls import path
from .views import DashboardView, SellerView, ClientDashboardView


app_name = 'dashboard'
urlpatterns = [

    path('dashboard/', DashboardView, name='dashboard'),
path('seller/', SellerView, name='seller_dashboard'),
path('dashboard/', ClientDashboardView, name='client_dashboard'),
]
