from django.urls import path
from . import views

app_name = 'products-api'

urlpatterns = [
    # path('', views.ProductMixinView.as_view(), name='create'),
    path('', views.ProductListCreateAPIView.as_view(), name='create'),
    path('<int:pk>/update/', views.ProductUpdateAPIView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ProductDeleteAPIView.as_view(), name='delete'),
    path('<int:pk>/', views.ProductDetailAPIView.as_view(), name='detail'),
]
