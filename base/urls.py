from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('room/<int:id>/', views.room, name='room'),
    path('profile/<int:id>/', views.userProfile, name='profile'),
    
    
    path('allRoom/', views.allRoom, name='allRoom'),
    path('create_room/', views.createRoom, name='create_room'),
    path('update_room/<int:id>/', views.updateRoom, name='update_room'),
    path('delete_room/<int:id>/', views.deleteRoom, name='delete_room'),
    path('deleteMessage/<int:id>/', views.deleteMessage, name='deleteMessage'),
]