from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm
# Create your views here.

# rooms = [
#     { "id":"1", "name": "java Room"},
#     { "id":"2", "name": "python Room"},
#     { "id":"3", "name": "javascript Room"},
    
# ]

def home(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "base/home.html", context=context)

def room(request, id):
    # room =  None
    # for i in rooms:
    #     if id == int(i["id"]):
    #         room = i
    room = Room.objects.get(id= id)
    context = {"room": room}
    return render(request, "base/room.html", context=context)
    

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, "base/room_form.html", context=context)
    
    
def updateRoom(request, id):
    room = Room.objects.get(id= id)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, "base/room_form.html", context=context)

def deleteRoom(request, id):
    room = Room.objects.get(id= id)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room':room}
    return render(request, "base/delete.html", context=context)