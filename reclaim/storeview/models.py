from django.db import models

from accounts.models import User


# Create your models here.
class Store_Structure(models.Model):
    store_structure_id = models.AutoField(primary_key=True)
    store_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # デフォルト値を設定
    store_name = models.CharField(max_length=100)
    floor = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    space = models.CharField(max_length=100)
    def __str__(self):
        return str(self.store_name)