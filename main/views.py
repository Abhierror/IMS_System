from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy 
from .forms import ProductForm, CategoryForm, SupplierForm, CustomerForm
from .models import Product, Category, Supplier, Customer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'home/about.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# ------------ Category -----------------
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'main/category_list.html'
    context_object_name = 'categories'

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'main/category_delete.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'main.delete_category'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Category Deleted Successfully.")
        except ProtectedError:
            messages.error(request, "Cannot delete this category because it is linked to other records.")
            return redirect(self.success_url)

        return redirect(self.success_url)
    
# ------------ Supplier -----------------
class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'main/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'main/supplier_list.html'
    context_object_name = 'suppliers'

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'main/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

class SupplierDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'main/supplier_delete.html'
    success_url = reverse_lazy('supplier_list')
    permission_required = 'main.supplier_delete'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Supplier Deleted Successfully.")
        except ProtectedError:
            messages.error(request, "Cannot delete this supplier because it is linked to other records.")
            return redirect(self.success_url)

        return redirect(self.success_url)
   
# ------------ Product -----------------
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'main/product_list.html'
    context_object_name = 'products'

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'main/product_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'main.product_delete'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Product Deleted successfully.")
        except ProtectedError:
            messages.error(request, "Cannot delete this product because it is linked to other records.")
            return redirect(self.success_url)
        
        return redirect(self.success_url)

# ------------ Customer -----------------
class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'main/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'main/customer_list.html'
    context_object_name = 'customers'

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'main/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Customer
    template_name = 'main/customer_delete.html'
    success_url = reverse_lazy('customer_list')
    permission_required = 'main.customer_delete'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Customer Delete Successfully.")
        except ProtectedError:
            messages.error(request, "Cannot delete this customer as it is connected to other records.")
            return redirect(self.success_url)
    
        return redirect(self.success_url)