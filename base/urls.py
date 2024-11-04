from django.urls import path
from .views import indexview

app_name = 'base'
urlpatterns = [
    path('', indexview, name='index'),
]