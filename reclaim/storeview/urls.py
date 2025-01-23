from django.urls import path

from . import views
from .views import detail_item_view, hello, registerform

app_name = 'storeview'
urlpatterns = [
    path('', views.index, name='index'),
    path('hello/', hello, name='hello'),
    path('registerform/', registerform, name='registerform'),
    # path('list/', item_list_view, name='list'),
    path('detail/<int:pk>/', views.detail_item_view, name='detail'),
    path('item/<int:pk>/', detail_item_view, name='item_detail'),
    path('update/<int:pk>/', views.update_item_view, name='update'),
    path('overview/', views.overview, name='overview'),
]
