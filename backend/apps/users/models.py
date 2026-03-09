from django.db import models
from django.contrib.auth.models import User


class Business(models.Model):
    """Business/Tenant model for multi-tenant CRM"""
    owner = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='business'
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default='')
    email = models.EmailField(blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return self.name
