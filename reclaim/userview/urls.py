from django.urls import path
from .views import  item_list_view, detail_item_view
from . import views

app_name = 'userview'
urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.detail_item_view, name='detail'),
    path('item/<int:pk>/', detail_item_view, name='item_detail'),
]