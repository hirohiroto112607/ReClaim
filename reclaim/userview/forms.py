from django import forms
from items.models import item_message, item


class ItemContactForm(forms.ModelForm):
    class Meta:
        model = item_message
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': '5',
                'placeholder': '落とし物に関する詳細な情報をお書きください',
                'class': 'form-control'
            })
        }
        error_messages = {
            'message': {
                'required': 'メッセージを入力してください。'
            }
        }


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = item
        fields = ['item_image']
        labels = {
            'item_image': '画像',
        }