from urllib.parse import parse_qs

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from items.models import item, item_message
from django.db.models import Q
from django.contrib import messages

from .forms import ItemContactForm
import json
import unicodedata

# Create your views here.

def index(request):
    object_list = item.objects.all()
    print(object_list)
    return render(request, 'userview/list.html', {'object_list': object_list})


def item_list_view(request):
    object_list = item.objects.all()
    return render(request, 'userview/list.html', {'object_list': object_list})


def detail_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    
    # 各フィールドのユニコード正規化
    decoded_data = {
        'name': unicodedata.normalize('NFKC', item_instance.item_name),
        'description': unicodedata.normalize('NFKC', item_instance.item_description),
        'location': unicodedata.normalize('NFKC', item_instance.item_lost_location),
    }
    
    # JSON データが存在する場合はデコード
    if item_instance.ai_generated_keywords:
        try:
            ai_json = json.loads(item_instance.ai_generated_keywords)
            decoded_data['ai_keywords'] = ai_json["keywords"]
        except json.JSONDecodeError:
            decoded_data['ai_keywords'] = None
    
    context = {
        'item': item_instance,
        'decoded': decoded_data,
    }
    print(context)
    return render(request, 'userview/item_detail.html', context)


def contact(request, pk):
    if request.method == "POST":
        item_instance = get_object_or_404(item, pk=pk)
        initial_data = {'email': request.user.email}
        form = ItemContactForm(request.POST)
        if form.is_valid():
            message_instance = form.save(commit=False)
            message_instance.item_id = item_instance
            message_instance.email = request.user.email
            message_instance.save()
            messages.success(request, 'メッセージが正常に送信されました。')
            return redirect('userview:detail', pk=pk)
    else:
        item_instance = get_object_or_404(item, pk=pk)
        initial_data = {'email': request.user.email}
        form = ItemContactForm(initial=initial_data)
    
    return render(request, 'userview/contact.html', {
        'form': form,
        'item_instance': item_instance
    })

def search_page(request):
    return render(request, 'userview/search.html')

def search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        print(query)
        if query:
            object_list = item.objects.filter(
                Q(ai_generated_keywords__icontains=query) |
                Q(item_description__icontains=query) |
                Q(item_name__icontains=query) |
                Q(item_category_id__category_name__icontains=query)
            )
            return render(request, 'userview/search.html', {'object_list': object_list, 'query': query})
        else:
            return redirect('userview:index')
    else:
        return redirect('userview:index')