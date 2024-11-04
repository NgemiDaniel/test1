from django.urls import path
from .views import deposit_funds, user_balance, manage_wallet, verify_payment, confirm_payment
app_name = 'payment'
urlpatterns = [
    path('deposit/', deposit_funds, name='deposit_funds'),
    path('balance/', user_balance, name='user_balance'),
    path('manage-wallet/', manage_wallet, name='manage_wallet'),
    path('verify-payments/', verify_payment, name='verify_payments'),
    path('confirm-payment/<str:transaction_id>/', confirm_payment, name='confirm_payment'),
]