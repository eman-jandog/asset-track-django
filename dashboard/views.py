from datetime import date, datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView, View
from django.db.models import Q, Count, Sum
from django.db.models.functions import Coalesce, ExtractMonth
from numerize import numerize
from rest_framework.views import APIView
from rest_framework import status
from activity.selectors import get_recent_activities
from .models import Asset, Order, OrderItem, Staff
from . import forms


@login_required
def home(request):
    return render(request, 'dashboard/index.html')

class OverviewSection(View):
    template_name = 'dashboard/sections/overview.html'
    today = date.today()

    def get_assets_count(self):
        assets = Asset.objects.aggregate(
            total=Count("name"),
            current_month=Count("name", filter=Q(date_purchase__month=self.today.month)),
        )

        last_month_total = assets["total"] - assets["current_month"]
        if last_month_total != 0:
            calc_percentage = (assets["current_month"] / last_month_total) * 100
            percentage_increase = round(calc_percentage, 2)
        else:
            percentage_increase = 0

        return {
            "total": assets["total"],
            "percentage": percentage_increase
        }

    def get_orders_count(self):
        return Order.objects.aggregate(
            active=Count("track_id", filter=Q(status="In Transit")), 
            pending=Count("track_id", filter=Q(status="Pending")),
            today=Count("track_id", filter=Q(date_ordered__date=self.today))
        )

    def get_staffs_count(self):
        return Staff.objects.aggregate(
            total=Count("id"),
            total_new_hires=Count("id",filter=Q(start_date__month=self.today.month))
        )

    def get_assets_value(self):
        month = self.today.month
        quarter = ((month-1) // 3) + 1

        assets = Asset.objects.aggregate(
            total_value=Sum("price"),
            current_quarter_value=Sum("price", filter=Q(date_purchase__quarter=quarter)) 
        )

        return {
            "value_total": numerize.numerize(assets["total_value"]),
            "current_quarter_value": numerize.numerize(assets["current_quarter_value"])
        }

    def setup_recent_activities(self):
        activities = get_recent_activities()
        return

    def get(self, request):
        assets_data = self.get_assets_count()
        orders_data = self.get_orders_count()
        staffs_data = self.get_staffs_count()
        assets_value_data = self.get_assets_value()
        activities = self.setup_recent_activities()
        
        context = {
            "assets": assets_data | assets_value_data,
            "orders": orders_data,
            "staffs": staffs_data,
            "recent_activities": activities
        }

        return render(request, self.template_name, context)

class StaffSection(View):
    template_name = 'dashboard/sections/staff.html'

    def get(self, request, pk=None):
        staff_qs = Staff.objects.prefetch_related('assets').all()

        query = request.GET.get("q")
        
        if query:
            staff_qs = staff_qs.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

        staff_qs = staff_qs.order_by('id')

        paginator = Paginator(staff_qs, 10)

        page = request.GET.get("page")

        try:
            staff_page = paginator.get_page(page)
        except (EmptyPage, PageNotAnInteger):
            staff_page = paginator.get_page(1)
        
        context = {
            'staff_page': staff_page,
        }

        if query is not None or page is not None:
            self.template_name = 'dashboard/tables/staffs_table.html'

        return render(request, self.template_name, context)

class OrderSection(View):
    template_name = 'dashboard/sections/orders.html'

    def get(self, request):
        order_qs = Order.objects.prefetch_related('items').all()

        query = request.GET.get('q')

        if query:
            order_qs = order_qs.filter(
                Q(items__item__icontains=query) |
                Q(supplier__icontains=query) |
                Q(track_id__icontains=query)
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
            self.template_name = 'dashboard/tables/orders_table.html'
        
        return render(request, self.template_name, context)

class AssetSection(View):
    template_name = 'dashboard/sections/assets.html'

    def get(self, request):
        asset_qs = Asset.objects.prefetch_related("employee").all()
        query = request.GET.get('q')
        if query:
            query = query.strip()
            asset_qs = asset_qs.filter(
                Q(name__icontains=query) |
                Q(track_id__icontains=query) |
                Q(location__icontains=query) |
                Q(category__icontains=query) |
                Q(employee__first_name__icontains=query) |
                Q(employee__last_name__icontains=query)
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
            self.template_name = 'dashboard/tables/assets_table.html'

        return render(request, self.template_name, context)

class AssetForm(View):
    template_name = 'dashboard/forms/asset_form.html'
 
    def get(self, request, pk=None):

        if pk:
            asset = Asset.objects.get(pk=pk)
        else:
            asset = None
            
        form = forms.AssetForm(instance=asset)

        context = {
            'form': form,
            'asset': asset 
        }

        return render(request, self.template_name, context)
    
    def post(self, request, pk=None):

        if pk:
            asset = get_object_or_404(Asset, pk=pk)
        else:
            asset = None

        form = forms.AssetForm(request.POST, instance=asset)

        context = {
            'form': form
        }

        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=404)

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

            return HttpResponse(status=201)  

        else:
            return HttpResponse(status=400)

    def delete(self, request, pk):
        order =  get_object_or_404(Order, pk=pk)
        order.delete()
        return HttpResponse(status=204)

class StaffForm(View):
    template_name = 'dashboard/forms/staff_form.html'

    def get(self, request, pk=None):
        if pk:
            staff = get_object_or_404(Staff, pk=pk)
        else:
            staff = None
        form = forms.StaffForm(instance=staff)
        context = {
            'form': form,
            'staff': staff
        }
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        if pk:
            staff = get_object_or_404(Staff, pk=pk)
        else:
            staff = None

        form = forms.StaffForm(request.POST, instance=staff)
        
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
            print("Invalid form!")

class GetChartsData(View):
    
    def get_asset_distribution(self):
        categories = Asset.ASSET_CATEGORY
        count_qs = Asset.objects.values("category").annotate(total=Count("id"))
        count_map = { row["category"]:  row["total"] for row in count_qs}
        labels = [ label for _, label in categories ]
        values = [ count_map.get(key, 0) for key, _ in categories ]
        return {"labels": labels,"values": values}

    def get_monthly_orders(self):
        order_qs = Order.objects.annotate(month=ExtractMonth("date_ordered")).values("month").annotate(total=Count("month"))
        order_map = { row["month"]: row["total"] for row in order_qs }
        labels = [ datetime(2000, m, 1).strftime('%b') for m in range(1,13) ]
        values = [ order_map.get(m,0) for m in range(1,13)]
        return {"labels": labels, "values": values}

    def get(self, request):
        pie = self.get_asset_distribution()
        line = self.get_monthly_orders()
        return JsonResponse({
            "pie": pie,
            "line": line
        })

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
