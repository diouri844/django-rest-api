from django.db import models


# let create  a customer profile related to auth user : 


# users/models.py
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    USER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
    ]
    
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    ]
    
    # Link to Django User (one-to-one)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    
    # Role and Type
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='individual')
    
    # Contact Info
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Company specific fields (optional, only for companies)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    ice = models.CharField(max_length=50, blank=True, null=True, help_text="ICE number (for companies)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user_type == 'company' and self.company_name:
            return f"{self.company_name} ({self.user.username})"
        return f"{self.user.get_full_name() or self.user.username}"
    
    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'