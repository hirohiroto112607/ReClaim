import python.GenAi as GenAi
from django.shortcuts import get_object_or_404, redirect, render
from items.models import item, item_category, tag
import json
from .forms import RegisterForm

# Create your views here.


def index(request):
    object_list = item.objects.all()
    tag_list = tag.objects.all()
    print(tag_list)
    return render(request, 'storeview/list.html', {'object_list': object_list, 'tag_list': tag_list})


def hello(request):
    hw = 'Hello World!'
    return render(request, 'base.html', {'object': hw})


def registerform(request):
    tag_object_list = tag.objects.all()
    item_category_object_list = item_category.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            item_instance = form.save()
            return redirect('storeview:index')
    else:
        form = RegisterForm()
    return render(request, 'storeview/form.html', {'form': form, 'tag_object_list': tag_object_list, 'item_category_object_list': item_category_object_list})


def detail_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    return render(request, 'storeview/item_detail.html', {'item': item_instance})


def update_item_view(request, pk):
    tag_object_list = tag.objects.all()
    item_category_object_list = item_category.objects.all()
    item_instance = item.objects.get(item_id=pk)
    form = RegisterForm(instance=item_instance)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            item_instance = form.save()
            return redirect('storeview:detail', pk=item_instance.pk)
    else:
        form = RegisterForm(instance=item_instance)
    print(item.objects.get(pk=1))
    return render(request, 'storeview/upd-form.html', {'form': form, 'item_instance': item_instance, 'tag_object_list': tag_object_list, 'item_category_object_list': item_category_object_list})


def overview(request):
    object_list = item.objects.all()
    return render(request, 'storeview/overview.html', {'object_list': object_list})


def AiGenerate(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    form = RegisterForm(instance=item_instance)
    tag_object_list = tag.objects.all()
    item_category_object_list = item_category.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # item_instance = 
            form.save()
            return redirect('storeview:detail', pk=item_instance.pk)
    else:
        form = RegisterForm(instance=item_instance)
    image_path = str(item_instance.item_image)
    # test = GenAi.generate_by_image_path("", image_path).text
    test = '[ "アウター", "コート", "ロングコート", "ダブルブレスト", "ピーコート", "オーバーコート", "チェスターコート", "キャメル", "ベージュ", "無地", "シンプル", "秋冬", "レディース", "ファッション", "通勤", "きれいめ", "カジュアル", "フォーマル", "上品", "エレガント", "着回し", "オフィス", "デート", "普段着", "ジャケット", "長袖", "ポケット付き", "ボタン留め", "ウール", "上着", "冬服", "秋服", "防寒", "保温性", "暖か", "膝丈", "ミドル丈", "ゆったり", "リラックス", "シルエット", "定番", "ベーシック", "マニッシュ", "きれいめカジュアル", "大人女子", "着痩せ", "スタイルアップ", "トレンド", "人気", "おしゃれ", "コーディネート", "着こなし" ]'
    parsed = json.loads(test)
    return render(request, 'storeview/AiGenerate.html', {'item_instance': item_instance, 'gen': parsed, 'form': form, 'tag_object_list': tag_object_list, 'item_category_object_list': item_category_object_list})


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
