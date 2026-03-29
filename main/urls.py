from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('home/about-us/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ---------------- Category ---------------
    path('category/add', views.CategoryCreateView.as_view(), name='add_category'),  
    path('category/category-list/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # ---------------- Supplier ---------------
    path('supplier/add', views.SupplierCreateView.as_view(), name='add_supplier'), 
    path('supplier/supplier-list/', views.SupplierListView.as_view(), name='supplier_list'),
    path('supplier/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('supplier/<int:pk>/edit', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    
    # ---------------- Product ---------------
    path('product/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('product/products-list/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/edit', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # ---------------- Customer ----------------------
    path('customer/add', views.CustomerCreateView.as_view(), name='add_customer'),
    path('customer/customer-list/', views.CustomerListView.as_view(), name='customer_list'),
    path('customer/<int:pk>/edit', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/<int:pk>/delete', views.CustomerDeleteView.as_view(), name='customer_delete'),

    # ---------------- Stock Addition -----------------
    path('add-stock/', views.StockTransactionCreateView.as_view(), name='add_stock'),
    path('transaction-list', views.StockTransactionListView.as_view(), name='transaction_list'),
    path('add-sale/', views.sale_creation, name='add_sale'),
]
