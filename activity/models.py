from django.db import models
from django.conf import settings

# Create your models here.
class Activity(models.Model):
    ACTIVITY_TYPES = [
        ("asset", "Asset"),
        ("order", "Order"),
        ("staff", "Staff"),
        ("system", "System")
    ]

    type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPES
    )
    
    action = models.CharField(
        max_length=100
    )

    message = models.TextField()

    related_object_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    related_object_type = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f'self.message'