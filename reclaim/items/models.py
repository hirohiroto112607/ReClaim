from accounts.models import User
from django.conf import settings
from django.db import models
from django.shortcuts import render, redirect
from django.db.models import Q
import unicodedata
from django.utils import timezone


# Create your models here.
class item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_category_id = models.ForeignKey('item_category', on_delete=models.PROTECT, null=True, blank=True)
    item_name = models.CharField(max_length=100, null=True, blank=True)
    item_date = models.DateTimeField(default=None, null=True, blank=True)
    item_lost_location = models.CharField(max_length=100, null=True, blank=True)
    item_description = models.TextField(null=True, blank=True)
    item_image = models.ImageField(upload_to='images/', null=True, blank=True)
    item_status = models.BooleanField(default=False)
    item_founder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    ai_generated_keywords = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.item_name)


class item_category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.category_name)
    
class item_message(models.Model):
    message_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey('item', on_delete=models.CASCADE)
    email = models.EmailField(max_length=254,)
    message = models.TextField(max_length=500,)
    def __str__(self):
        return str(self.message)

