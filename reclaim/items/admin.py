from django.contrib import admin
from .models import item, item_category, item_message

admin.site.register(item)
admin.site.register(item_category)
admin.site.register(item_message)
