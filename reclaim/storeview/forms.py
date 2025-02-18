from django import forms
from django.db import models
from django.forms import ModelForm
from items.models import item


class RegisterForm(ModelForm):
    class Meta:
        model = item
        item_id = models.AutoField(primary_key=True)
        item_category_id = models.ForeignKey(
            'item_category', on_delete=models.PROTECT, blank=True, null=True)
        item_name = models.CharField(max_length=100, blank=True, null=True)
        # item_date = models.DateTimeField()
        item_lost_location = models.CharField(max_length=100)
        item_description = models.TextField(blank=True, null=True)
        item_image = models.ImageField(
            upload_to='images/', blank=True, null=True)
        item_status = models.BooleanField(default=False)
        item_founder = models.CharField(max_length=100)
        fields = ['item_category_id',
                  'item_name', 
                  'item_date',
                  'item_lost_location', 'item_description', 'ai_generated_json', 'item_image', 'item_status', 'item_founder']
        labels = {
            'item_category_id': 'カテゴリー',
            'item_name': '名前',
            'item_date': '発見日時',
            'item_lost_location': '発見場所',
            'item_description': '説明文',
            'ai_generated_json': 'キーワード',
            'item_image': '画像',
            'item_status': '発見されたか',
            'item_founder': '発見者',
        }


class ImageUploadForm(forms.ModelForm):
    item_date = forms.DateField(
        label='発見日時',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    
    class Meta:
        model = item
        fields = ['item_image', 'item_date']
        labels = {
            'item_image': '画像',
        }
        help_texts = {
            'item_image': 'アップロードする画像を選択してください。',
        }
        error_messages = {
            'item_image': {
                'invalid': '有効な画像ファイルをアップロードしてください。',
                'required': '画像のアップロードは必須です。',
            },
        }
