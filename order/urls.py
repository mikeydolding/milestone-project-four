from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_order, name='view_order'),
    path('add/<order_item_id>/', views.add_to_order, name='add_to_order'),
    #path('adjust/<order_item_id>/', views.adjust_order, name='adjust_order'),
    #path('remove/<order_item_id>/', views.remove_from_order, name='remove_from_order'),
]
