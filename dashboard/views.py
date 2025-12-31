from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView, View
from django.db.models import Q, Count
from rest_framework.views import APIView
from rest_framework import status
from .models import Asset, Order, OrderItem
from . import forms


@login_required
def home(request):
    # user = request.user
    '''
    if not user.is_staff or not user.is_superuser:
        orders = Order.objects.select_related('product').filter(staff=user.id)
        products = None
    else:
        orders = Order.objects.values('product__name', 'order_quantity')
        products = Product.objects.values('name', 'quantity')
        
    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-home')
    else:
        form = forms.OrderForm()

    context = {
        'orders': orders,
        'form': form,   
        'products': products
    }
    '''
    return render(request, 'dashboard/index.html')

def overview(request):
    return render(request, 'dashboard/sections/overview.html')

def staff(request):
    return render(request, 'dashboard/sections/staff.html')

def orders(request):
    order_qs = Order.objects.prefetch_related('items').all()

    query = request.GET.get('q')

    if query:
        order_qs = order_qs.filter(
            Q(items__item__icontains=query) |
            Q(supplier__icontains=query) |
            Q(order_id__icontains=query)
        )
    
    order_qs = order_qs.order_by('id')

    total_pending = order_qs.filter(status="Pending").count()
    total_inTransit = order_qs.filter(status="In Transit").count()
    total_delivered = order_qs.filter(status="Delivered").count()

    paginator = Paginator(order_qs, 10)

    page = request.GET.get('page')
    try:
        order_page = paginator.get_page(page)
    except (EmptyPage, PageNotAnInteger):
        order_page = paginator.get_page(1)

    context = {
        'page_obj': order_page,
        'query': query,
        'totalPending': total_pending,
        'totalInTransit': total_inTransit,
        'totalDelivered': total_delivered
    }

    if page is not None or query is not None:
        return render(request, 'dashboard/tables/orders_table.html', context)
    
    return render(request, 'dashboard/sections/orders.html', context)

def assets(request):
    asset_qs = Asset.objects.all()

    query = request.GET.get('q')
    if query:
        query = query.strip()
        asset_qs = asset_qs.filter(
            Q(name__icontains=query) |
            Q(track_id__icontains=query) |
            Q(location__icontains=query) |
            Q(category__icontains=query)
        )
        
    asset_qs = asset_qs.order_by('id')

    paginator = Paginator(asset_qs, 10)
    page = request.GET.get('page')
    try:
        asset_page = paginator.get_page(page)
    except (EmptyPage, PageNotAnInteger):
        asset_page = paginator.get_page(1)

    context = {
        'page_obj': asset_page,
        'query': query
    }

    if query is not None or page is not None:
        return render(request, 'dashboard/tables/assets_table.html', context)

    return render(request, 'dashboard/sections/assets.html', context)

class AssetForm(View):
    template_name = 'dashboard/forms/asset_form.html'
 
    def get(self, request, pk=None):

        if pk:
            asset = Asset.objects.get(pk=pk)
            id = asset.id
            self.template_name = 'dashboard/forms/asset_form_update.html'
        else:
            asset = None
            id = None
            
        form = forms.AssetForm(instance=asset)

        context = {
            'form': form,
            'id': id
        }

        return render(request, self.template_name, context)
    
    def post(self, request, pk=None):

        if pk:
            asset = get_object_or_404(Asset, pk=pk)
            form = forms.AssetForm(request.POST, instance=asset)
        else:
            form = forms.AssetForm(request.POST)

        context = {
            'form': form
        }

        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        else:
            return render(request, self.template_name, status=500)

    def delete(self, request, pk):
        asset = get_object_or_404(Asset, pk=pk)
        asset.delete()
        return HttpResponse(status=204)

class OrderForm(View):
    template_name = 'dashboard/forms/order_form.html'

    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk)
            form = forms.OrderForm(instance=order)
            formset = forms.OrderItemFormSet(instance=order)
            formset.extra = 0
            self.template_name = 'dashboard/forms/order_form_update.html'
        else:
            order = None
            form = forms.OrderForm()
            formset = forms.OrderItemFormSet()
        
        context = {
            'form': form,
            'formset':  formset,
            'order': order  
        }

        return render(request, self.template_name, context)

    def post(self, request, pk=None):

        if pk:
            order = get_object_or_404(Order, pk=pk)
        else:
            order = None
        
        form = forms.OrderForm(request.POST, instance=order)
        
        formset = forms.OrderItemFormSet(request.POST, instance=order)

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()  

            if request.headers['HX-Request']:
                return HttpResponse(status=201)  

        else:
            context = {
                'form': form,
                'formset':  formset
            }

            return render(request, self.template_name, context, status=400)

    def delete(self, request, pk):
        order =  get_object_or_404(Order, pk=pk)
        order.delete()
        return HttpResponse(status=204)

@login_required
def _staff(request):
    users = User.objects.all()

    context = {
        'users': users
    }

    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request, id):
    user = User.objects.select_related('profile').get(id=id)

    context = {
        'user': user
    }

    return render(request,'dashboard/staff_detail.html', context)

@login_required
def order(request):
    orders = Order.objects.select_related('staff').all()

    for order in orders:
        order.date_ordered = order.date_ordered.strftime('%m-%d-%Y')

    context = {
        'orders': orders
    }

    return render(request, 'dashboard/order.html', context)

@login_required
def order_cancel(request, id):
    if request.method == 'POST':
        item = Order.objects.get(id=id)
        item.delete()
        return redirect('dashboard-home')

@login_required
def _asset(request):
    assets = Asset.objects.all()

    if request.method == 'POST':
        product_form = forms.ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            return redirect('dashboard-assets')
    else:
        product_form = forms.ProductForm()
    
    context = {
        'products': products,
        'product_form': product_form    
    }

    return render(request, 'dashboard/product.html', context)

@login_required
def product_delete(request, id):
    if request.method == 'POST':
        try:
            asset = Asset.objects.get(id=id)
            asset.delete()
        except Exception as e:
            print(e.message)
    
    return redirect('dashboard-product')

@login_required
def product_update(request, id):
    asset = Asset.objects.get(id=id)

    if request.method == "POST":
        update_form = forms.ProductForm(request.POST,instance=asset)
        if update_form.is_valid():
            update_form.save()
            return redirect('dashboard-product')
    else:
        update_form = forms.ProductForm(instance=asset)
        
    context = {
        'form': update_form
    }

    return render(request,'dashboard/product_update.html', context)

class AboutView(TemplateView): 
    template_name = "dashboard/about.html"
