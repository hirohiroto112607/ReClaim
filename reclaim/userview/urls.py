from django.urls import path

from . import views
from .views import detail_item_view, item_list_view, contact

app_name = 'userview'
urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.detail_item_view, name='detail'),
    path('item/<int:pk>/', detail_item_view, name='item_detail'),
    path('detail/<int:pk>/contact/', contact, name='contact'),
]