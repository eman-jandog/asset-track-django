from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Staff(models.Model):
    DEPARTMENT_CHOICES = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resource'),
        ('ADMIN', 'Administrative'),
        ('FINANCE', 'Accounting & Finance'),
        ('OPS', 'Operational')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, null=True)
    position = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=11, null=True)
    start_date = models.DateField(null=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Asset(models.Model):
    ASSET_CATEGORY = [
        ('IE', 'IT Equipment'),
        ('MB', 'Mobiles Devices'),
        ('OF', 'Office Furnitures'),
        ('OS', 'Office Supplies'),
        ('NE', 'Network Equipment'),
        ('SL', 'Software & Licenses'),
        ('EE', 'Electrical Equipement'),
        ('SS', 'Security Systems'),
        ('MISC', 'Miscellaneous')
    ]

    STATUS_CATEGORY = [
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Retired', 'Retired')
    ]

    name = models.CharField(max_length=100)
    employee = models.ForeignKey(User, on_delete=models.PROTECT, related_name="assets", null=True)
    track_id = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=50, choices=ASSET_CATEGORY, null=True)
    brand = models.CharField(max_length=50,null=True, blank=True)
    sn = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True)
    date_purchase = models.DateField(null=True)
    date_warranty = models.DateField(null=True)
    status = models.CharField(max_length=50, choices=STATUS_CATEGORY, default='Available')
    location = models.CharField(max_length=200, null=True, blank=True)
    supplier = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    last_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):

    STATUS_CATEGORY = [
        ('Delivered', 'Delivered'),
        ('In Transit', 'In Transit'),
        ('Pending', 'Pending')
    ]

    DEPARTMENT_CHOICES = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resource'),
        ('ADMIN', 'Administrative'),
        ('FINANCE', 'Accounting & Finance'),
        ('OPS', 'Operational')
    ]

    track_id = models.CharField(max_length=50, null=True)
    supplier = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CATEGORY, null=True, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_expected = models.DateField(null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    instruction = models.TextField(null=True)

    def __str__(self):
        return f'{self.track_id}'

    def get_items(self):
        return self.items.all()

    def get_total(self):
        total = sum(item.total() for item in self.get_items())
        return total.quantize(Decimal('0.01'))

class OrderItem(models.Model):
    item = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=2, null=True, default=0)
    quantity = models.PositiveIntegerField(null=True) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True, related_name='items')

    def __str__(self):
        return f'{self.item}'   

    def total(self):
        return self.price * self.quantity