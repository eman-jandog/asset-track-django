from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.db.models import Q
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
    order_qs = Order.objects.prefetch_related('orderitem_set').all()

    for order in order_qs:
        print(order.orderitem_set.all())

    
    paginator = Paginator(order_qs, 10)

    page = request.GET.get('page')
    try:
        order_page = paginator.get_page(page)
    except (EmptyPage, PageNotAnInteger):
        order_page = paginator.get_page(1)

    context = {
        'page_obj': order_page,
        'query': '',
        'data': order_qs
    }

    if page is not None:
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

class AssetForm(APIView):

    def get(self, request, format=None):
        form = forms.AssetForm()
        return render(request, 'dashboard/forms/asset_form.html', {'form': form})
    
    def post(self, request, format=None):
        form = forms.AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)

class AssetFormDetail(APIView):

    def get(self, request, id, format=None):
        asset = get_object_or_404(Asset, id=id)
        form = forms.AssetForm(instance=asset)
        return render(request, 'dashboard/forms/asset_form_update.html', {'form': form, 'id': id})

    def post(self, request, id, format=None):
        asset = get_object_or_404(Asset, id=id)
        form = forms.AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)

    def delete(self, request, id, format=None):
        asset = get_object_or_404(Asset, id=id)
        asset.delete()
        return HttpResponse(status=204)

class OrderForm(CreateView):
    model = Order
    form_class = forms.OrderForm
    template_name = 'dashboard/forms/order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = forms.OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = forms.OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        self.object = form.save()

        formset.instance = self.object

        if formset.is_valid():
            formset.save()

            if self.request.headers['Hx-Request']:
                # Option 1: Return nothing → just close modal
                response = HttpResponse("")
                response.status_code = 201
                # response['HX-Trigger'] = 'orderCreated'  # Trigger event for JS

                # Option 2: Return success message (nice feedback)
                # response = render(self.request, 'orders/partials/success_message.html')
                # response['HX-Trigger'] = 'orderCreated'

                # # Option 3 (Most Common): Re-render empty form so user can add another
                # context = self.get_context_data()
                # context['form'] = OrderForm()  # Clean main form
                # context['formset'] = OrderItemFormSet()  # One empty row
                # response = render(self.request, self.template_name, context)
                # response['HX-Retarget'] = '#order-modal-content'  # If inside 
                
                return response

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


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
