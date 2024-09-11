from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
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
    room_message = Message.objects.filter(Q(room__topic__name__icontains= q))
    room_count = rooms.count()
    context = {"rooms": rooms, 'topics': topics, 'room_count': room_count, "room_message": room_message}
    return render(request, "base/home.html", context=context)

def room(request, id):
    # room =  None
    # for i in rooms:
    #     if id == int(i["id"]):
    #         room = i
    room = Room.objects.get(id= id)
    room_message = room.message_set.all()
    
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', id = room.id)
    
    participants = room.participants.all()
    
    context = {"room": room, "room_message": room_message, "participants": participants}
    return render(request, "base/room.html", context=context)

def userProfile(request, id):
    user =  User.objects.get(id= id)
    rooms = user.room_set.all
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "rooms":rooms,"room_message":room_message, "topics":topics}
    return render(request, "base/profile.html", context=context)

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
            room = form.save(commit=False)
            room.host = request.user
            room.save()
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
    context = {'obj':room}
    return render(request, "base/delete.html", context=context)

# @login_required(login_url= 'login')
# def writeMessage(request):
#     if request.method == 'POST':
#         room_message = request.POST.get('body')
#         if room_message.is_valid():
#             room_message.save()
#             return redirect('')
#     context = {'room_message':room_message}
#     return render(request, "base/room.html", context=context)

@login_required(login_url='login')
def deleteMessage(request, id):
    message = Message.objects.get(id=id)
    room = message.room
    
    if request.user != message.user:
        return HttpResponse('You are not allowed.')
    
    if request.method == 'POST':
        message.delete()

        # Check if the user has any other messages in the room
        user_messages_in_room = room.message_set.filter(user=request.user)
        print(user_messages_in_room.count())
        print("umar")

        # If the user has no more messages in the room, remove them from participants
        if not user_messages_in_room:
            room.participants.remove(request.user)

        return redirect('room', id=room.id)

    context = {'obj': message}
    return render(request, "base/delete.html", context=context)
