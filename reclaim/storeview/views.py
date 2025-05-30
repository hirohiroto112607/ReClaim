import json
import unicodedata
import unicodedata

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
    
    # 各フィールドのユニコード正規化
    decoded_data = {
        'name': unicodedata.normalize('NFKC', item_instance.item_name),
        'description': unicodedata.normalize('NFKC', item_instance.item_description),
        'location': unicodedata.normalize('NFKC', item_instance.item_lost_location),
    }
    
    # JSON データが存在する場合はデコード
    if item_instance.ai_generated_json:
        try:
            ai_json = json.loads(item_instance.ai_generated_json)
            decoded_data['ai_json'] = ai_json["keywords"]
        except json.JSONDecodeError:
            decoded_data['ai_json'] = None
    
    context = {
        'item': item_instance,
        'decoded': decoded_data,
    }
    print(context)
    return render(request, 'storeview/item_detail.html', context)


def update_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    item_category_object_list = item_category.objects.all()

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES,
                            instance=item_instance)
        if form.is_valid():
            form.save()
            item_instance.save()
            return redirect('storeview:index')
    else:
        form = RegisterForm(instance=item_instance)

    # 各フィールドのユニコード正規化
    decoded_data = {
        'name': unicodedata.normalize('NFKC', item_instance.item_name),
        'description': unicodedata.normalize('NFKC', item_instance.item_description),
        'location': unicodedata.normalize('NFKC', item_instance.item_lost_location),
    }

    # JSON データが存在する場合はデコード
    if item_instance.ai_generated_json:
        try:
            ai_json = json.loads(item_instance.ai_generated_json)
            decoded_data['ai_json'] = ai_json  # デコードしたJSONをそのまま渡す
        except json.JSONDecodeError:
            decoded_data['ai_json'] = None

    return render(request, 'storeview/upd-form.html', {
        'form': form,
        'item_instance': item_instance,
        'item_category_object_list': item_category_object_list,
        'decoded': decoded_data,
    })


def overview(request):
    object_list = item.objects.all()
    return render(request, 'storeview/overview.html', {'object_list': object_list})


def AiGenerate(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    # 既存のJSONデータがある場合は、それを解析して重複を防ぐ
    if (item_instance.ai_generated_json):
        try:
            existing_data = json.loads(item_instance.ai_generated_json)
            if isinstance(existing_data, str):
                existing_data = json.loads(existing_data)
        except json.JSONDecodeError:
            existing_data = []
    else:
        existing_data = []
    
    # 新しいAI生成データを取得
    new_data = GenAi.process_ai_generate(item_instance.pk, str(item_instance.item_image))
    
    # データの整形と重複の除去
    if isinstance(new_data, str):
        try:
            new_data = json.loads(new_data)
        except json.JSONDecodeError:
            new_data = []
    
    # リストの場合は重複を除去して保存
    if isinstance(new_data, list):
        # すべての要素から余分な引用符を除去
        cleaned_data = [tag.strip("'") for tag in new_data]
        # 重複を除去
        unique_data = list(set(cleaned_data))
        # JSONとして保存
        item_instance.ai_generated_json = json.dumps(unique_data, ensure_ascii=False)
        item_instance.save()
    
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
        if query:
            # Unicode正規化
            query = unicodedata.normalize('NFKC', query)
            print(query)
            object_list = item.objects.filter(
                Q(ai_generated_json__icontains=query) |
                Q(item_description__icontains=query) |
                Q(item_name__icontains=query) | # type: ignore
                Q(item_category_id__category_name__icontains=query)
            )
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
        if form.is_valid() and request.FILES:
            item_instance = form.save(commit=False)
            item_instance.item_founder = request.user

            # POSTデータから直接値を取得
            item_instance.item_date = request.POST.get('item_date')
            item_instance.item_lost_location = request.POST.get(
                'item_lost_location')
            item_instance.item_name = "未分類アイテム"
            item_instance.item_description = "画像認識による自動分類を待機中"
            # ItemCategoryが存在することを確認してから設定
            item_instance.item_category_id = item_category.objects.get(
                category_id=9)

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
