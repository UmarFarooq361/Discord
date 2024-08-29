from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:id>', views.room, name='room'),
    path('create_room', views.createRoom, name='create_room'),
    path('update_room/<int:id>/', views.updateRoom, name='update_room'),
    path('delete_room/<int:id>/', views.deleteRoom, name='delete_room'),
]