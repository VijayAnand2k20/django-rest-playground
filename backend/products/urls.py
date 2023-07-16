from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListCreateAPIView.as_view(), name='create'),
    path('<int:pk>/update/', views.ProductUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProductDeleteAPIView.as_view(), name='delete'),
    path('<int:pk>/', views.ProductDetailAPIView.as_view(), name='detail'),
]
