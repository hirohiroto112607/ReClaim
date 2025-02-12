from django.urls import path

from . import views
from .views import contact, detail_item_view, item_list_view

app_name = 'userview'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.detail_item_view, name='detail'),
    path('item/<int:pk>/', detail_item_view, name='item_detail'),
    path('detail/<int:pk>/contact/', contact, name='contact'),
    path('search_page/', views.search_page, name='search_page'),
    path('search/', views.search, name='search'),
]