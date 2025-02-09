import json

import python.GenAi as GenAi
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from items.models import item, item_category, tag
from django.db.models import Q

from .forms import RegisterForm

# Create your views here.
GenAi.init()


def index(request):
    object_list = item.objects.all()
    tag_list = tag.objects.all()
    return render(request, 'storeview/list.html', {'object_list': object_list, 'tag_list': tag_list})


def hello(request):
    hw = 'Hello World!'
    return render(request, 'base.html', {'object': hw})


def registerform(request):
    tag_object_list = tag.objects.all()
    item_category_object_list = item_category.objects.all()
    item_instance = None
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES,
                            instance=item_instance)
        if form.is_valid():
            item_instance = form.save()
            return redirect('storeview:index')
    else:
        form = RegisterForm()
    return render(request, 'storeview/form.html', {
        'form': form,
        'tag_object_list': tag_object_list,
        'item_category_object_list': item_category_object_list
    })


def detail_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    return render(request, 'storeview/item_detail.html', {'item': item_instance})


def update_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    tag_object_list = tag.objects.all()
    item_category_object_list = item_category.objects.all()

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES,
                            instance=item_instance)
        if form.is_valid():
            form.save()
            return redirect('storeview:index')
    else:
        form = RegisterForm(instance=item_instance)

    return render(request, 'storeview/upd-form.html', {
        'form': form,
        'item_instance': item_instance,
        'tag_object_list': tag_object_list,
        'item_category_object_list': item_category_object_list,
    })


def overview(request):
    object_list = item.objects.all()
    return render(request, 'storeview/overview.html', {'object_list': object_list})


def AiGenerate(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    tag_object_list = tag.objects.all()
    item_category_object_list = item_category.objects.all()
    gen = None  # ここで初期化

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES, instance=item_instance)
        if form.is_valid():
            obj = form.save()
            return redirect('storeview:detail', pk=obj.pk)
        else:
            # エラーがある場合は AiGenerate.html を再レンダリング
            gen = item_instance.item_keyword
            return render(request, 'storeview/AiGenerate.html', {
                'item_instance': item_instance,
                'gen': gen,
                'form': form,
                'tag_object_list': tag_object_list,
                'item_category_object_list': item_category_object_list
            })
    else:
        form = RegisterForm(instance=item_instance)
        try:
            response = GenAi.generate_by_image_path(image_path=item_instance.item_image)
            gen = response
        except Exception as error:
            print("Error: " + str(error))
            gen = "AI生成が制限されています。後ほど再度お試しください。"
        return render(request, 'storeview/AiGenerate.html', {
            'item_instance': item_instance,
            'gen': gen,
            'form': form,
            'tag_object_list': tag_object_list,
            'item_category_object_list': item_category_object_list
        })


def delete_item(request, pk):
    if request.method == 'POST':
        item_instance = get_object_or_404(item, item_id=pk)
        item_instance.delete()
        return redirect('storeview:index')
    else:
        return redirect('storeview:index')


def search_page(request):
    return render(request, 'storeview/search.html')


def search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        print(query)
        if query:
            object_list = item.objects.filter(
                Q(item_keyword__icontains=query) | Q(item_description__icontains=query))
            return render(request, 'storeview/search.html', {'object_list': object_list})
        else:
            return redirect('storeview:index')
    else:
        return redirect('storeview:index')


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
