from django.contrib import admin
from .models import Category, Customer, Supplier, AuditLog, Product, Sale, StockTransaction, SaleItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']
    search_fields = ['category_name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','product_name', 'category', 'supplier', 'selling_price', 'reorder_level', 'created_at']
    search_fields = ['id','product_name', 'category__category_name', 'supplier__supplier_name']
    list_filter = ['supplier', 'category', 'created_at']
    autocomplete_fields = ['supplier', 'category']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id','supplier_name', 'contact_person', 'city', 'state', 'phone_number', 'email']
    search_fields = ['id','supplier_name', 'email','city', 'state', 'postal_code']
    list_filter = ['city', 'state']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','customer_name', 'phone_number', 'email', 'city', 'state']
    search_fields = ['id','city', 'state', 'email', 'customer_name']
    list_filter = ['state', 'city']

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['id','product', 'transaction_type', 'quantity', 'supplier', 'customer', 'transaction_date']
    search_fields = ['id','product__product_name', 'supplier__supplier_name', 'customer__customer_name', 'remarks']
    list_filter = ['transaction_type', 'transaction_date', 'created_by']
    date_hierarchy = 'transaction_date'
    autocomplete_fields = ['supplier', 'customer', 'product', 'created_by']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice_number', 'customer', 'sale_date','total_amount', 'payment_method', 'payment_status', 'created_by']
    search_fields = ['id', 'invoice_number', 'customer__customer_name']
    list_filter = ['sale_date', 'payment_method', 'payment_status', 'created_by', 'created_at']
    date_hierarchy = 'sale_date'
    autocomplete_fields = ['created_by', 'customer']


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'sale_id', 'product_id', 'quantity', 'quantity', 'total_price']
    search_fields = ['id', 'sale_id__invoice_number',
    'product_id__product_name']
    list_filter = ['created_at']
    autocomplete_fields = ['product_id', 'sale_id']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'model_name', 'description', 'timestamp']
    search_fields = ['description']
    list_filter = ['user', 'action_type', 'model_name', 'timestamp']



