import json

import python.GenAi as GenAi
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from items.models import item, item_category
from django.db.models import Q
from django.contrib import messages

from .forms import RegisterForm
from .forms import ImageUploadForm

# Create your views here.


def index(request):
    object_list = item.objects.all()
    return render(request, 'storeview/list.html', {'object_list': object_list})


# def hello(request):
#     hw = 'Hello World!'
#     return render(request, 'base.html', {'object': hw})


def registerform(request):
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
        'item_category_object_list': item_category_object_list
    })


def detail_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    return render(request, 'storeview/item_detail.html', {'item': item_instance})


def update_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
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
        'item_category_object_list': item_category_object_list,
    })


def overview(request):
    object_list = item.objects.all()
    return render(request, 'storeview/overview.html', {'object_list': object_list})


def AiGenerate(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    GenAi.process_ai_generate(
        item_instance.pk, str(item_instance.item_image))
    return redirect('storeview:index')


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
                Q(ai_generated_json__icontains=query) | Q(item_description__icontains=query) | Q(item_name__icontains=query) | Q(item_category_id__category_name__icontains=query))
            return render(request, 'storeview/search.html', {'object_list': object_list, 'query': query})
        else:
            return redirect('storeview:index')
    else:
        return redirect('storeview:index')


def item_list_view(request):
    object_list = item.objects.all()
    return render(request, 'storeview/list.html', {'object_list': object_list})


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid() and request.FILES != None:    
            item_instance = form.save(commit=False)
            item_instance.item_founder = request.user  # 現在のユーザーを設定
            item_instance.save()
            # バックグラウンドでAIに送信する
            GenAi.process_ai_generate(
                item_instance.pk, str(item_instance.item_image))
            messages.success(request, '画像がアップロードされ、AIに送信されました。')
            return redirect('storeview:index')
        else:
            messages.error(request, '画像のアップロードに失敗しました。')
    else:
        form = ImageUploadForm()
    return render(request, 'storeview/upload_image.html', {'form': form})


'''
以下がカテゴリー名のリストです：
	定期券・カード類
	傘
	鍵
	文具・書類
	衣類・アクセサリー
	かばん・バッグ
	財布・貴重品
	電子機器
	その他
'''
