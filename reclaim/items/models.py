from accounts.models import User
from django.conf import settings
from django.db import models


# Create your models here.
class item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_category_id = models.ForeignKey('item_category', on_delete=models.PROTECT)
    # item_tag_id = models.ForeignKey('tag', on_delete=models.PROTECT)
    # item_tag_id = models.ManyToManyField('tag') #TODO
    item_name = models.CharField(max_length=100)
    item_date = models.DateTimeField()
    item_lost_location = models.CharField(max_length=100)
    item_description = models.TextField()
    item_image = models.ImageField(upload_to='images/', blank=True, null=True)
    item_status = models.BooleanField(default=False)
    item_founder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.item_name)


class item_category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.category_name)

class tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    # tag_type = models.ForeignKey('tag_type', on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=100)
    
#     def __str__(self):
#         return str(self.tag_name)

# class tag_type(models.Model):
#     tag_type_id = models.AutoField(primary_key=True)
#     tag_type_name = models.CharField(max_length=100)
#     def __str__(self):
#         return str(self.tag_type_name)
    
class item_message(models.Model):
    message_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey('item', on_delete=models.CASCADE)
    email = models.EmailField(max_length=254,)
    message = models.TextField(max_length=500,)
    def __str__(self):
        return str(self.message)
    
class item_keyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey('item', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=200)
    def __str__(self):
        return str(self.keyword)
