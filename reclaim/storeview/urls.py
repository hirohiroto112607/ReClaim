from django.urls import path

from . import views

app_name = 'storeview'
urlpatterns = [
    path('', views.index, name='index'),
    path('hello/', views.hello, name='hello'),
    path('registerform/', views.registerform, name='registerform'),
    path('list/', views.item_list_view, name='list'),
    path('detail/<int:pk>/', views.detail_item_view, name='detail'),
    path('item/<int:pk>/', views.detail_item_view, name='item_detail'),
    path('update/<int:pk>/', views.update_item_view, name='update'),
    path('overview/', views.overview, name='overview'),
    path('AiGenerate/<int:pk>', views.AiGenerate, name='AiGenerate'),
    path('delete/<int:pk>', views.delete_item, name='delete'),
    path('search_page/', views.search_page, name='search_page'),
    path('search/', views.search, name='search'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('display_json/<int:pk>/', views.display_json, name='display_json'),
    path('item_list/', views.item_list_view, name='item_list'),  # 追加
]
