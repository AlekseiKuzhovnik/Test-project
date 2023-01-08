from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventUser
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import CreateEvent
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def elists(request):
    user = request.user.id
    all_event_id = EventUser.objects.filter(user_id=user).order_by('-id')
    array = [int(i.event_id) for i in all_event_id]
    events = [Event.objects.filter(id=i) for i in array]
    context = {
        'events': events
    }
    return render(request, 'elists/main_elists.html', context)


class EventDetailView(DetailView):
    model = Event


class UserEventListView(ListView):
    model = Event
    template_name = 'elists/user_events.html'
    context_object_name = 'elists'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Event.objects.filter(event_creator_id=user.id).order_by('-create_date')


def create_event(request):
    if request.method == "POST":
        form = CreateEvent(request.POST, request.FILES)
        if form.is_valid():
            event = Event()
            event.event_name = form.cleaned_data['event_name']
            event.short_description = form.cleaned_data['short_description']
            event.full_description = form.cleaned_data['full_description']
            event.event_creator_id = request.user.id
            event.image = form.cleaned_data['image']
            event.save()

            event_users = EventUser()
            event_users.event_id = event.id
            event_users.user_id = request.user.id
            event_users.save()

            return redirect('event-detail', pk=event.id)
            # return redirect('elists')
    else:
        form = CreateEvent()
    return render(request, 'elists/create_event.html', {'form': form})
