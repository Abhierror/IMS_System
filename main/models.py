from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum, Case, When, IntegerField, F
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField("Enter product category.", max_length=50, unique=True)
    description = models.CharField("Enter category description.", max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['category_name']
    

class Product(models.Model):
    product_name = models.CharField("Enter product name.", max_length=100)
    SKU = models.CharField("Enter product SKU.", max_length=10, unique=True, db_index=True)
    category = models.ForeignKey(
        'Category', 
        on_delete=models.PROTECT,
        related_name='products'
    )
    sub_category = models.CharField("Enter the sub-category of the product.", max_length=50, null=True, blank=True)
    supplier = models.ForeignKey(
        'Supplier', 
        on_delete=models.PROTECT,
        related_name='products'
    )
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reorder_level = models.PositiveIntegerField(default=10)
    product_description = models.CharField("Enter product description.", max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} ({self.SKU})"
    
    def get_current_stock(self):
            return self.transactions.aggregate(
                total=Sum(
                    Case(
                        When(transaction_type='IN', then='quantity'),
                        When(transaction_type='OUT', then=-1 * models.F('quantity')),
                        output_field=IntegerField()
                    )
                ) 
            )['total'] or 0
    
    def clean(self):
        if self.selling_price < self.cost_price:
            raise ValidationError("Selling price cannot be less than cost price.")
    
    class Meta:
        ordering = ["product_name"]

    def get_absolute_url(self):
        return reverse("product-detail", args=[str(self.id)])
    
    
class Supplier(models.Model):
    supplier_name = models.CharField("Enter supplier name." ,max_length=50)
    contact_person = models.CharField("Enter supplier's contact person name.", max_length=100)
    phone_number = models.CharField("Enter contact person phone number.", max_length=10, unique=True, null=True, blank=True)
    email = models.EmailField("Enter contact person email address.", max_length=30, unique=False)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.supplier_name or "Unnamed Supplier" 
    
    class Meta:
        ordering = ['supplier_name']

    def get_absolute_url(self):
        return reverse("supplier-detail", args=[str(self.id)])
    
class Customer(models.Model):
    customer_name = models.CharField("Enter customer name." ,max_length=50)
    phone_number = models.CharField("Enter customer's phone number.", max_length=10, unique=True, null=True, blank=True)
    email = models.EmailField("Enter customer email address.", max_length=30, unique=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name
    
    class Meta:
        ordering = ["customer_name"]

    def get_absolute_url(self):
        return reverse("customer-detail", args=[str(self.id)])

class StockTransaction(models.Model):
    product = models.ForeignKey(
        'Product', 
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    stock_status = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out')
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=stock_status,
        default="IN"
    )
    quantity = models.PositiveIntegerField()
    transaction_date = models.DateField(auto_now_add=True)
    supplier = models.ForeignKey(
        'Supplier', 
        on_delete=models.SET_NULL,
        related_name="transactions",
        blank=True,
        null=True
    )
    customer = models.ForeignKey(
        'Customer', 
        on_delete=models.SET_NULL, 
        related_name='transactions',
        null=True,
        blank=True
    )
    reference_number = models.UUIDField(default=uuid.uuid4, unique=True)
    remarks = models.CharField("Enter remarks if any.", max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.RESTRICT,
        related_name='transactions' 
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} ({self.transaction_type}) - Qty: {self.quantity}"
    
    def clean(self):
        if self.transaction_type == 'IN' and not self.supplier:
            raise ValidationError("Stock IN must have a supplier.")

        if self.transaction_type == 'OUT' and not self.customer:
            raise ValidationError("Stock OUT must have a customer.") 

    class Meta:
        ordering = ["-transaction_date"]
    
class Sale(models.Model):
    invoice_number = models.CharField(max_length=10, unique=True, db_index=True)
    customer = models.ForeignKey(
        'Customer', 
        on_delete=models.PROTECT, 
        related_name='sales',
        blank=True, 
        null=True
    )
    sale_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_options = (
        ('NETB', 'Net Banking'),
        ('CARD', 'Debit Card / Credit Card'),
        ('UPI', 'UPI')
    )
    payment_method = models.CharField(
        max_length=20,
        choices=payment_options,
    )
    payment_status_op = (
        ('DUE', 'On Due'),
        ('PROCESSING', 'Processing'),
        ('PAID', 'Paid')
    )
    payment_status=models.CharField(
        max_length=15,
        choices=payment_status_op
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.RESTRICT,
        related_name='sales'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice_number} - {self.sale_date} - {self.total_amount}"
    
    class Meta:
        ordering = ["-sale_date"]

    def get_absolute_url(self):
        return reverse("sale-detail", args=[str(self.id)])

class SaleItem(models.Model):
    sale_id = models.ForeignKey('Sale', on_delete=models.PROTECT, related_name = 'sale_items')
    product_id = models.ForeignKey('Product', on_delete=models.PROTECT, related_name='sale_items')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sale_id} - {self.quantity} - {self.total_price}"
    
    class Meta:
        ordering = ['-created_at']

class AuditLog(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.RESTRICT,
        related_name='audit_log'    
    )
    action = (
        ('C', 'Create'),
        ('U', 'Update'),
        ('D', 'Delete')
    )
    action_type = models.CharField(
        max_length=10,
        choices=action,
        default='C'
    )
    model_name = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    description = models.CharField(max_length=150, help_text="Describe the action performed.", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action_type}"
    
    class Meta:
        ordering = ["-timestamp"]
