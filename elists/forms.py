from django import forms
from .models import Event


class CreateEvent(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('event_name', 'short_description', 'full_description', 'start_date', 'end_date', 'image')

