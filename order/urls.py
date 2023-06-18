from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_order, name='view_order'),
    path('add/<orderItem_id>/', views.add_to_order, name='add_to_order'),
    path('update/<orderItem_id>/', views.update_order, name='update_order'),
    path('remove/<orderItem_id>/', views.remove_from_order, name='remove_from_order'),
]
