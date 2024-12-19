from django.urls import path
from .views import hello,  registerform, item_list_view, detail_item_view
from . import views

app_name = 'storeview'
urlpatterns = [
    path('', views.index, name='index'),
    path('hello/', hello, name='hello'),
    path('registerform/', registerform, name='registerform'),
    # path('list/', item_list_view, name='list'),
    path('detail/<int:pk>/', views.detail_item_view, name='detail'),
    path('item/<int:pk>/', detail_item_view, name='item_detail'),
    path('update/<int:pk>/', views.update_item_view, name='update'),
]
