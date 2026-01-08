from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    DEPARTMENT_CHOICES = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resource'),
        ('ADMIN', 'Administrative'),
        ('FINANCE', 'Accounting & Finance'),
        ('OPS', 'Operational')
    ]
    
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, null=True)
    position = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=11, null=True)
    image = models.ImageField(default='avatar.png', upload_to='profile_images')
    bio = models.TextField(null=True)
    start_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.staff.username.capitalize()}-Profile'