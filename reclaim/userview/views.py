from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from items.models import item, item_category, tag, tag_type
from .forms import ItemContactForm
from django.http import HttpResponseRedirect
from items.models import item_message
from urllib.parse import parse_qs

# Create your views here.


def test(request):
    object_list = item.objects.all()
    print(tag_type)
    return render(request, 'userview/test.html', {'object_list': object_list})


def index(request):
    object_list = item.objects.all()
    print(object_list)
    return render(request, 'userview/list.html', {'object_list': object_list})


def item_list_view(request):
    object_list = item.objects.all()
    return render(request, 'userview/list.html', {'object_list': object_list})


def detail_ite