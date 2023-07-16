from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.product_alt_view, name='detail'),
    path('', views.product_alt_view, name='create'),
]
