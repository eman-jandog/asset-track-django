from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework import status
from .models import Asset, Order
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
    return render(request, 'dashboard/sections/orders.html')

def assets(request):
    assets = Asset.objects.all()
    return render(request, 'dashboard/sections/assets.html', {'assets': assets})

class AssetForm(APIView):

    def get(self, request, format=None):
        form = forms.AssetForm()
        return render(request, 'dashboard/forms/asset_form.html', {'form': form})
    
    def post(self, request, format=None):
        form = forms.AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Success!'}, status=201)

class AssetFormAction(APIView):

    def get(self, request, id, format=None):
        asset = get_object_or_404(Asset, id=id)
        form = forms.AssetForm(instance=asset)
        return render(request, 'dashboard/forms/asset_form.html', {'form': form})

    def post(self, request, id, format=None):
        asset = get_object_or_404(Asset, id=id)
        form = forms.AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Success'}, status=status.HTTP_200_OK)

    def delete(selt, request, id, format=None):
        asset = get_object_or_404(Asset, id=id)
        asset.delete()
        return redirect('dashboard-assets')

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
    orders = Order.objects.select_related('asset','staff').all()

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
