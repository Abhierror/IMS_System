from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy 
from .forms import ProductForm, CategoryForm, SupplierForm, CustomerForm, StockTransactionForm, SaleForm, SaleItemForm
from django.forms import formset_factory
from .models import Product, Category, Supplier, Customer, StockTransaction, AuditLog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError, Q
from django.db import transaction
from django.db.models.functions import Lower, Concat
from .mixin import AuditMixin

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'home/about.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# ------------ Category -----------------
class CategoryCreateView(LoginRequiredMixin, AuditMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/category_form.html'
    success_url = reverse_lazy('category_list')

    audit_action = 'C'

    def get_audit_description(self, obj):
        return f"{self.request.user} performed {self.action_type} in {obj}"

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'main/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(category_name__icontains=query)

        return queryset
    paginate_by = 10

class CategoryUpdateView(LoginRequiredMixin, AuditMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/category_form.html'
    success_url = reverse_lazy('category_list')

    audit_action = 'U'

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, AuditMixin, DeleteView):
    model = Category
    template_name = 'main/category_delete.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'main.delete_category'

    audit_action = 'D'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            messages.success(request, "Category Deleted Successfully.")
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Cannot delete this category because it is linked to other records.")
            return redirect(self.success_url)
    
# ------------ Supplier -----------------
class SupplierCreateView(LoginRequiredMixin, AuditMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'main/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

    audit_action = 'C'

class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'main/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        city = self.request.GET.get('city')

        if query:
            queryset = queryset.filter(
                Q(supplier_name__icontains=query) |
                Q(contact_person__icontains=query) |
                Q(city__icontains=query) |
                Q(state__icontains=query)
            )

        if city:
            queryset = queryset.filter(city__icontains=city)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = Supplier.objects.values_list('city', flat=True).distinct()
        return context
            
class SupplierUpdateView(LoginRequiredMixin, AuditMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'main/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

    audit_action = 'U'

class SupplierDeleteView(LoginRequiredMixin, PermissionRequiredMixin, AuditMixin, DeleteView):
    model = Supplier
    template_name = 'main/supplier_delete.html'
    success_url = reverse_lazy('supplier_list')
    permission_required = 'main.supplier_delete'

    audit_action = 'D'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            messages.success(request, "Supplier Deleted Successfully.")
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Cannot delete this supplier because it is linked to other records.")
            return redirect(self.success_url)
   
# ------------ Product -----------------
class ProductCreateView(LoginRequiredMixin, AuditMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('product_list')

    audit_action = 'C'

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'main/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        supplier = self.request.GET.get('supplier')
        
        if query:
            queryset = queryset.filter(
                Q(product_name__icontains=query) |
                Q(SKU__icontains=query) |
                Q(category__category_name__icontains=query) |
                Q(supplier__supplier_name__icontains=query) 
            )
        
        if category: 
            queryset = queryset.filter(category__category_name=category)

        if supplier:
            queryset = queryset.filter(supplier__supplier_name=supplier)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Product.objects.values_list('category__category_name', flat=True).distinct()
        context['suppliers'] = Product.objects.values_list('supplier__supplier_name', flat=True).distinct()
        return context

class ProductUpdateView(LoginRequiredMixin, AuditMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('product_list')

    audit_action = 'U'

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, AuditMixin, DeleteView):
    model = Product
    template_name = 'main/product_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'main.product_delete'

    audit_action = 'D'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            messages.success(request, "Product Deleted successfully.")
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Cannot delete this product because it is linked to other records.")
            return redirect(self.success_url)

# ------------ Customer -----------------
class CustomerCreateView(LoginRequiredMixin, AuditMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'main/customer_form.html'
    success_url = reverse_lazy('customer_list')

    audit_action = 'C'

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'main/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        queryset =  super().get_queryset()
        query = self.request.GET.get('q')
        city = self.request.GET.get('city')
        state = self.request.GET.get('state')

        if query:
            queryset = queryset.filter(
                Q(customer_name__icontains = query) |
                Q(address__icontains = query) |
                Q(city__icontains = query) |
                Q(state__icontains = query)
            )

        if city:
            queryset = queryset.filter(city=city)
        if state:
            queryset = queryset.filter(state=state)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = Customer.objects.values_list('city', flat=True).distinct()
        context['states'] = Customer.objects.values_list('state', flat=True).distinct()
        return context

class CustomerUpdateView(LoginRequiredMixin, AuditMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'main/customer_form.html'
    success_url = reverse_lazy('customer_list')

    audit_action = 'U'

class CustomerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, AuditMixin, DeleteView):
    model = Customer
    template_name = 'main/customer_delete.html'
    success_url = reverse_lazy('customer_list')
    permission_required = 'main.customer_delete'

    audit_action = 'D'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            messages.success(request, "Customer Delete Successfully.")
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Cannot delete this customer as it is connected to other records.")
            return redirect(self.success_url)

# ---------------- Stock Addition ---------------
class StockTransactionCreateView(LoginRequiredMixin, AuditMixin, CreateView):
    model = StockTransaction 
    form_class = StockTransactionForm
    template_name = 'main/add_stock.html'
    success_url = reverse_lazy('product_list')

    audit_action = 'C'

    def form_valid(self, form):
        form.instance.transaction_type = 'IN'
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Stock Added Successfully!")
        return response

class StockTransactionListView(LoginRequiredMixin, ListView):
    model = StockTransaction
    template_name = 'main/StockTransactionList.html'
    context_object_name = 'StockTransactions'
    paginate_by = 10


# ---------------- Audit Log creation -------------
def create_audit_log(user, action, model_name, object_id, description):
    AuditLog.objects.create(
        user = user,
        action_type = action,
        model_name = model_name,
        object_id = object_id,
        description = description
    )    

# ---------------- Sale creation ---------------
@login_required
def sale_creation(request):
    SaleItemFormSet = formset_factory(SaleItemForm, extra=2)

    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)

        if sale_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    sale = sale_form.save(commit=False)
                    sale.created_by = request.user
                    sale.total_amount = 0
                    sale.save()

                    total = 0

                    for form in formset:
                        if not form.cleaned_data:
                            continue

                        item = form.save(commit=False)
                        item.sale = sale

                        product = item.product

                        if item.quantity > product.get_current_stock():
                            raise ValueError(f"Not enough stock for {product}")
                        
                        item.unit_price = product.selling_price
                        item.total_price = item.unit_price * item.quantity
                        item.save()

                        total += item.total_price

                        StockTransaction.objects.create(
                            product=product,
                            transaction_type='OUT',
                            quantity=item.quantity,
                            customer=sale.customer,
                            created_by=request.user
                        )

                    # ✅ Update total inside transaction
                    sale.total_amount = total
                    sale.save()

                    # ✅ Audit log inside transaction
                    create_audit_log(
                        user=request.user,
                        action='C',
                        model_name='Sale',
                        object_id=sale.id,
                        description=f"Sale {sale.invoice_number} created by {request.user}"
                    )

                messages.success(request, "Sale created successfully!")
                return redirect('dashboard')
                
            except ValueError as e:
                messages.error(request, str(e))
            
        else:
            messages.error(request, "Fix form errors")
        
    else:
        sale_form = SaleForm()
        formset = SaleItemFormSet()

    return render(request, 'main/add_sale.html', {
        'sale_form': sale_form,
        'formset': formset
    })


                

    
