from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_all_products,name='products'),
    path('products/<str:pk>/', views.get_product,name='product'),
    path('products/new', views.new_product,name='new_product'),
    path('products/update/<str:pk>/', views.update_product,name='update'),
    path('products/delete/<str:pk>/', views.delete_product,name='delete'),

]
