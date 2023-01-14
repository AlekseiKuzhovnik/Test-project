from django import forms
from django.core.exceptions import ValidationError
from .models import Event, EventPlan
from datetime import datetime, timedelta


class CreateEvent(forms.ModelForm):
    start_date = forms.DateTimeField(initial=datetime.today().strftime("%d.%m.%Y %H:%M"), label='Дата начала')
    end_date = forms.DateTimeField(initial=(datetime.today() + timedelta(hours=1)).strftime("%d.%m.%Y %H:%M"), label='Дата завершения')

    class Meta:
        model = Event
        fields = ('event_name', 'short_description', 'full_description', 'start_date', 'end_date', 'image')
        labels = {'event_name': 'Название*', 'short_description': 'Короткое описание*',
                  'full_description': 'Полное описание', 'image': 'Добавить изображение'}

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

    def clean_end_date(self):
        start_date_data = self.cleaned_data['start_date']
        end_date_data = self.cleaned_data['end_date']

        if start_date_data >= end_date_data:
            raise ValidationError("Дата завершения не может быть раньше даты начала")

        return end_date_data


class UpdateEvent(forms.ModelForm):
    start_date = forms.DateTimeField(initial=datetime.today().strftime("%d.%m.%Y %H:%M"), label='Дата начала')
    end_date = forms.DateTimeField(initial=(datetime.today() + timedelta(hours=1)).strftime("%d.%m.%Y %H:%M"), label='Дата завершения')

    class Meta:
        model = Event
        fields = ('event_name', 'short_description', 'full_description', 'start_date', 'end_date')
        labels = {'event_name': 'Название*', 'short_description': 'Короткое описание*',
                  'full_description': 'Полное описание'}

    def __init__(self, *args, **kwargs):

        super(UpdateEvent, self).__init__(*args, **kwargs)

        self.fields['event_name'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['short_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['full_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control form-control-sm'}, placeholder="yyyy-mm-dd hh:mi")
        self.fields['end_date'].widget.attrs.update({'class': 'form-control form-control-sm'}, placeholder="yyyy-mm-dd hh:mi")

    # def clean_end_date(self):
    #     start_date_data = self.cleaned_data['start_date']
    #     end_date_data = self.cleaned_data['end_date']
    #
    #     if start_date_data >= end_date_data:
    #         raise ValidationError("Дата завершения не может быть раньше даты начала")
    #
    #     return end_date_data


class UpdateImageEvent(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Event
        fields = ('image',)
        labels = {'image': 'Изменить изображение'}

    def __init__(self, *args, **kwargs):

        super(UpdateImageEvent, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})


class CreateEventPlan(forms.ModelForm):
    start_date = forms.DateTimeField(initial=datetime.today().strftime("%d.%m.%Y %H:%M"), label='Дата начала')
    end_date = forms.DateTimeField(initial=(datetime.today() + timedelta(hours=1)).strftime("%d.%m.%Y %H:%M"), label='Дата завершения')

    class Meta:
        model = EventPlan
        fields = ('plan_name', 'plan_short_description', 'plan_full_description', 'start_date', 'end_date')
        labels = {'plan_name': 'Название*', 'plan_short_description': 'Короткое описание',
                  'plan_full_description': 'Полное описание'}

    def __init__(self, *args, **kwargs):

        super(CreateEventPlan, self).__init__(*args, **kwargs)

        self.fields['plan_name'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['plan_short_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['plan_full_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control form-control-sm'}, placeholder="yyyy-mm-dd hh:mi")
        self.fields['end_date'].widget.attrs.update({'class': 'form-control form-control-sm'}, placeholder="yyyy-mm-dd hh:mi")

    def clean_end_date(self):
        start_date_data = self.cleaned_data['start_date']
        end_date_data = self.cleaned_data['end_date']

        if start_date_data >= end_date_data:
            raise ValidationError("Дата завершения не может быть раньше даты начала")

        return end_date_data
