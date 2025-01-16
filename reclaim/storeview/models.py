from django.db import models


# Create your models here.
class Store_Structure(models.Model):
  store_structure_id = models.AutoField(primary_key=True)
  store_name = models.CharField(max_length=100)
  floor = models.CharField(max_length=100)
  area = models.CharField(max_length=100)
  space = models.CharField(max_length=100)