from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from items.models import item, item_category, tag, tag_type

from .forms import RegisterForm

# Create your views here.

def index(request):
    object_list = item.objects.all()
    print(object_list)
    return render(request, 'storeview/list.html', {'object_list': object_list})


def item_list_view(request):
    object_list = item.objects.all()
    return render(request, 'storeview/list.html', {'object_list': object_list})


def hello(request):
    hw = 'Hello World!'
    return render(request, 'base.html', {'object': hw})

def registerform(request):
    object_list = item.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            item_instance = form.save()
            return redirect('storeview:detail', pk=item_instance.pk)
    else:
        form = RegisterForm()
    return render(request, 'storeview/form.html', {'form': form , 'category_list':item_category.objects.all()})



def detail_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    return render(request, 'storeview/item_detail.html', {'item': item_instance})

def update_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=item_instance)
        if form.is_valid():
            item_instance = form.save()
            return redirect('storeview:detail', pk=item_instance.pk)
    else:
        form = RegisterForm(instance=item_instance)
    return render(request, 'storeview/form.html', {'form': form, 'item': item_instance})

'''
以下がカテゴリー名のリストです：
	貴重品類（硬貨、紙幣、各種有価証券 等）
	電子機器類（スマホ、PC 等）
	衣類類（コート、マフラー 等）
    アクセサリー類（ピアス、指輪、ネックレス 等）
	鍵（家、車、ロッカー 等）
    カード（クレジットカード、キャッシュカード 等）
	カバン・バッグ類（リュック 等）
	書類（折り紙、 等）
	スポーツ用品類（ボール、 食品類（ガム、飴 等
'''