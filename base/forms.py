from django.forms import ModelForm
from .views import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ["host", "participants"]