from django.urls import path    
from . import views

urlpatterns = [
    path('overview/', views.home, name='dashboard-home'),    
    path('staff/', views.staff, name='dashboard-staff'),
    path('orders/', views.orders, name='dashboard-orders'),
    path('assets/', views.assets, name='dashboard-assets'),
    path('assets/form/', views.AssetForm.as_view(), name='dashboard-assets-form'),
    path('assets/form/<int:id>/', views.AssetFormAction.as_view(), name='dashboard-assets-form-action'),

    # # path('staff/', views.staff, name='staff'),
    # path('staff/detail/<int:id>', views.staff_detail, name='dashboard-staff-detail'),
    # path('order/', views.order, name='dashboard-order'),
    # path('order/cancel/<int:id>/', views.order_cancel, name='dashboard-order-cancel'),
    # path('product/', views.product, name='dashboard-product'),
    # path('product/delete/<int:id>/', views.product_delete, name='dashboard-product-delete'),
    # path('product/update/<int:id>/', views.product_update, name='dashboard-product-update'),
    # path('about/', views.AboutView.as_view())
]