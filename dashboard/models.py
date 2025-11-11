from django.db import models
from django.contrib.auth.models import User

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
    location = models.CharField(max_length=200, null=True)
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

    name = models.CharField(max_length=100, null=True, blank=True)
    employee = models.ForeignKey(Staff, on_delete=models.PROTECT, null=True, blank=True)
    track_id = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=50, choices=ASSET_CATEGORY, null=True, blank=True)
    brand = models.CharField(max_length=50,null=True, blank=True)
    sn = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    date_purchase = models.DateField(null=True, blank=True)
    date_warranty = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CATEGORY, default='Available', blank=True)
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
        ('Processing', 'Processing'),
        ('Pending', 'Pending')
    ]
    order_id = models.CharField(max_length=50, null=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True) 
    status = models.CharField(max_length=50, choices=STATUS_CATEGORY, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.asset}'
