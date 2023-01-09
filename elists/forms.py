from django import forms
from .models import Event
from datetime import datetime


class CreateEvent(forms.ModelForm):
    start_date = forms.DateTimeField(initial=datetime.now())
    end_date = forms.DateTimeField(initial=datetime.now())

    class Meta:
        model = Event
        fields = ('event_name', 'short_description', 'full_description', 'start_date', 'end_date', 'image')
        labels = {'event_name': 'Название', 'short_description': 'Короткое описание',
                  'full_description': 'Полное описание', 'start_date': 'Дата начала', 'end_date': 'Дата завершения',
                  'image': 'Добавить изображение'}

        # widgets = {
        #     'end_date:': forms.DateTimeInput(attrs={'class': 'form-control'}),
        #     # 'short_description:': forms.TextInput(attr={'class': 'form-control'}),
        #     # 'full_description:': forms.Textarea(attr={'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):

        super(CreateEvent, self).__init__(*args, **kwargs)

        self.fields['event_name'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['short_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['full_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control form-control-sm'}, placeholder="yyyy-mm-dd hh:mi")
        self.fields['end_date'].widget.attrs.update({'class': 'form-control form-control-sm'}, placeholder="yyyy-mm-dd hh:mi")
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
