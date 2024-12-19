# Register your models here.
from django.contrib import admin

from items.models import item, item_category, tag, tag_type

admin.site.register(item)
admin.site.register(item_category)
admin.site.register(tag)
admin.site.register(tag_type)