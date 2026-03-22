from django import forms
from .models import Product, Supplier, Customer, Sale, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__' 

        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'SKU': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '10',
                'placeholder': 'Enter SKU'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'sub_category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cost_price': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'reorder_level': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'product_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
        

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

        widgets = {
            'supplier_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter the supplier's contact person name."
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

class CustomerForm(forms.ModelForm):
    class Meta:    
        model = Customer
        fields = '__all__'
        
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }