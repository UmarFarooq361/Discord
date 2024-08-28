from django.shortcuts import render

# Create your views here.

rooms = [
    { "id":"1", "title": "java Room"},
    { "id":"2", "title": "python Room"},
    { "id":"3", "title": "javascript Room"},
    
]

def home(request):
    context = {"rooms": rooms}
    return render(request, "base/home.html", context=context)

def room(request, id):
    room =  None
    for i in rooms:
        if id == int(i["id"]):
            room = i
    context = {"room": room}
    return render(request, "base/room.html", context=context)