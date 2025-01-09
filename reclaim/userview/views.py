from urllib.parse import parse_qs

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from items.models import item, item_category, item_message, tag, tag_type

from .forms import ItemContactForm

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


def detail_item_view(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    return render(request, 'userview/item_detail.html', {'item': item_instance})


def contact(request, pk):
    item_instance = get_object_or_404(item, pk=pk)
    return render(request, 'userview/contact.html', {'contact': item_instance})

# TODO ここから下は書き換える


def contact(request, pk):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ItemContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            query_string = request.body.decode()
            parsed_query = parse_qs(query_string)
            print(parsed_query)
            # process the data in form.cleaned_data as required
            email = parsed_query['email'][0]
            item_id = parsed_query['item_id'][0]
            message = parsed_query['message'][0]
            item_instance = item.objects.get(pk=item_id)  # ここでitemインスタンスを取得
            item_message.objects.create(
                item_id=item_instance,  # itemインスタンスを割り当てる
                message=message,
                email=email
            )
        # ...
        # redirect to a new URL:
        return HttpResponseRedirect("/userview/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ItemContactForm()
        item_instance = get_object_or_404(item, pk=pk)
    return render(request, 'userview/contact.html', {'contact': item_instance})
