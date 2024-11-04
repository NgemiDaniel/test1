from django.urls import path
from .views import (
    EmployeeLoginView, ClientLoginView, SellerSignUpView, ClientSignUpView, ClientLogoutView,
    EmployeeLogoutView, manager_profile_view, seller_profile_view, client_profile_view, manager_user_update_view, client_user_update_view, seller_user_update_view,
manager_password_change_view, client_password_change_view, seller_password_change_view
)

app_name = 'account'

urlpatterns = [
    path('login/employee/', EmployeeLoginView.as_view(), name='employee_login'),
    path('logout/employee/', EmployeeLogoutView.as_view(), name='employee_logout'),
    path('login/client/', ClientLoginView.as_view(), name='client_login'),
    path('logout/client/', ClientLogoutView.as_view(), name='client_logout'),
    path('signup/seller/', SellerSignUpView.as_view(), name='seller'),
    path('signup/client/', ClientSignUpView.as_view(), name='client_signup'),
    path('profile/manager/', manager_profile_view, name='manager_profile'),
    path('profile/seller/', seller_profile_view, name='seller_profile'),
    path('profile/client/', client_profile_view, name='client_profile'),
    path('manager/profile/update/', manager_user_update_view, name='manager_user_update'),
    path('client/profile/update/', client_user_update_view, name='client_user_update'),
    path('seller/profile/update/', seller_user_update_view, name='seller_user_update'),
    path('manager/password/change/', manager_password_change_view, name='manager_password_change'),
    path('client/password/change/', client_password_change_view, name='client_password_change'),
    path('seller/password/change/', seller_password_change_view, name='seller_password_change'),
]
