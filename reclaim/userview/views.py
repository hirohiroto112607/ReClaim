from urllib.parse import parse_qs

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from items.models import item, item_message
from django.db.models import Q

from .forms import ItemContactForm

# Create your views here.


def test(request):
    object_list = item.objects.all()
    # print(tag_type)
    return render(request, 'userview/test.html', {'object_list': object_list})


def index(request):
    object_list = item.objects.all()
    print(object_list)
    return render(request, 'userview/list.html', {'object_list': object_list})


def item_list_view(request):
    object_list = item.objects.all()
    return render(request, 'userview/list.html', {'object_list': object_list})


def detail_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    return render(request, 'userview/item_detail.html', {'item': item_instance})


def contact(request, pk):
    if request.method == "POST":
        form = ItemContactForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            item_id = request.POST.get('item_id')
            message = request.POST.get('message')
            item_instance = item.objects.get(pk=item_id)
            item_message.objects.create(
                item_id=item_instance,
                message=message,
                email=email
            )
            return redirect('userview:detail', pk=item_id)
        else:
            # フォームが無効な場合、エラーメッセージを表示
            item_instance = get_object_or_404(item, pk=pk)
            return render(request, 'userview/contact.html', {'form': form, 'item_instance': item_instance})

    else:
        form = ItemContactForm()
        item_instance = get_object_or_404(item, pk=pk)
    return render(request, 'userview/contact.html', {'form': form, 'item_instance': item_instance})

def search_page(request):
    return render(request, 'userview/search.html')

def search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        print(query)
        if query:
            object_list = item.objects.filter(Q(item_keyword__icontains=query)|Q(item_description__icontains=query))
            return render(request, 'userview/search.html', {'object_list': object_list})
        else:
            return redirect('userview:index')
    else:
        return redirect('userview:index')