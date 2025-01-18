from django import forms
from items.models import item_message


class ItemContactForm(forms.Form):
     class Meta:
         model = item_message
         fields = ('email','message','item_id')