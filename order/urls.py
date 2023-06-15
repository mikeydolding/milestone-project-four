from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_order, name='view_order'),
    path('add/<orderItem_id>/', views.add_to_order, name='add_to_order'),
    #path('adjust/<orderItem_id>/', views.adjust_order, name='adjust_order'),
    #path('remove/<orderItem_id>/', views.remove_from_order, name='remove_from_order'),
]
