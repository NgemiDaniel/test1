from django.contrib.auth.decorators import login_required
from account.decorators import role_required
from django.shortcuts import render

# Create your views here.
@login_required
@role_required('manager')
def DashboardView(request):

    return render(request, 'dashboard/dashboard.html')
@login_required
@role_required('seller')
def SellerView(request):

    return render(request, 'dashboard/seller_dashboard.html')


@login_required
@role_required('client')
def ClientDashboardView(request):

    return render(request, 'dashboard/client_dashboard.html')