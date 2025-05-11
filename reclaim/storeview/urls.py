from django.urls import path

from . import views

app_name = 'storeview'
urlpatterns = [
    path('', views.item_list_view, name='index'),
    path('registerform/', views.registerform, name='registerform'),
    path('about/', views.index, name='about'),
    path('detail/<int:pk>/', views.detail_item_view, name='detail'),
    path('item/<int:pk>/', views.detail_item_view, name='item_detail'),
    path('update/<int:pk>/', views.update_item_view, name='update'),
    path('overview/', views.overview, name='overview'),
    path('AiGenerate/<int:pk>', views.AiGenerate, name='AiGenerate'),
    path('delete/<int:pk>', views.delete_item, name='delete'),
    path('search_page/', views.search_page, name='search_page'),
    path('search/', views.search, name='search'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('messages/', views.message_list_view, name='messages'),
]
