from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.ProductDetailAPIView.as_view(), name='detail'),
    path('', views.ProductListCreateAPIView.as_view(), name='create'),
]
