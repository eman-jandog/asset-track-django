from django.contrib import admin
from .models import Asset, Order

admin.site.site_header = 'Admin Panel'

class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'track_id')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('asset', 'staff')


admin.site.register(Asset, AssetAdmin)
admin.site.register(Order, OrderAdmin)
