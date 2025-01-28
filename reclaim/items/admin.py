# Register your models here.
from django.contrib import admin
from .models import item, item_category, item_message, tag
# ,tag_type

admin.site.register(item)
admin.site.register(item_category)
admin.site.register(tag)
# admin.site.register(tag_type)
admin.site.register(item_message)
