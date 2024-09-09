from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# rooms = [
#     { "id":"1", "name": "java Room"},
#     { "id":"2", "name": "python Room"},
#     { "id":"3", "name": "javascript Room"},
# ]

def login_page(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username= username)
        except:
            messages.error(request, "User does not exists.")
            
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User or Password incorrect.")
    context = {'page':page}
    return render(request, "base/login_register.html", context=context)
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'Error occurs during registration')
    context = {'form':form}
    return render(request, "base/login_register.html", context=context)
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {"rooms": rooms, 'topics': topics, 'room_count': room_count}
    return render(request, "base/home.html", context=context)

def room(request, id):
    # room =  None
    # for i in rooms:
    #     if id == int(i["id"]):
    #         room = i
    room = Room.objects.get(id= id)
    context = {"room": room}
    return render(request, "base/room.html", context=context)

def allRoom(request):
    allRoom = Room.objects.all()
    context = {"allRoom": allRoom}
    return render(request, "base/allRoom.html", context=context)
    
@login_required(login_url= 'login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, "base/room_form.html", context=context)
    

@login_required(login_url= 'login')
def updateRoom(request, id):
    room = Room.objects.get(id= id)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed.')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, "base/room_form.html", context=context)

@login_required(login_url= 'login')
def deleteRoom(request, id):
    room = Room.objects.get(id= id)
    if request.user != room.host:
        return HttpResponse('You are not allowed.')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room':room}
    return render(request, "base/delete.html", context=context)