from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventUser
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from .forms import CreateEvent, UpdateEvent, UpdateImageEvent
# from django.views.generic import (
#     ListView,
#     DetailView,
#     CreateView,
#     UpdateView,
#     DeleteView
# )


def elists(request):
    user = request.user.id
    all_event_id = EventUser.objects.filter(user_id=user).order_by('-id')
    array = [int(i.event_id) for i in all_event_id]
    events = [Event.objects.filter(id=i) for i in array]
    context = {
        'events': events
    }
    return render(request, 'elists/main_elists.html', context)


# class EventDetailView(DetailView):
#     model = Event


# class UserEventListView(ListView):
#     model = Event
#     template_name = 'elists/user_events.html'
#     context_object_name = 'elists'
#     paginate_by = 5
#
#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Event.objects.filter(event_creator_id=user.id).order_by('-create_date')


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
            event.start_date = form.cleaned_data['start_date']
            event.end_date = form.cleaned_data['end_date']
            event.save()

            event_users = EventUser()
            event_users.event_id = event.id
            event_users.user_id = request.user.id
            event_users.save()

            return redirect('event_detail', pk=event.id)
            # return redirect('elists')
    else:
        form = CreateEvent()
    return render(request, 'elists/create_event.html', {'form': form})


def event_detail(request, pk):
    event_inf = get_object_or_404(Event, pk=pk)
    user_name = User.objects.get(id=event_inf.event_creator_id)
    return render(request, 'elists/event_detail.html', context={'event': event_inf, 'user_name': user_name})


def event_update(request, pk):
    if request.method == 'POST':
        form = UpdateEvent(request.POST, request.FILES)
        if form.is_valid():
            event_inf = get_object_or_404(Event, pk=pk)
            event = Event()
            event.id = event_inf.id
            event.event_name = form.data['event_name']
            event.short_description = form.data['short_description']
            event.full_description = form.data['full_description']
            event.create_date = event_inf.create_date
            event.event_creator_id = event_inf.event_creator_id
            event.image = event_inf.image
            event.is_closed = event_inf.is_closed
            event.start_date = form.data['start_date']
            event.end_date = form.data['end_date']
            event.save()
            return redirect('event_detail', pk=event.id)
    else:
        event_inf = get_object_or_404(Event, pk=pk)
        user_name = User.objects.get(id=event_inf.event_creator_id)
        form = UpdateEvent()
        form.initial['event_name'] = event_inf.event_name
        form.initial['short_description'] = event_inf.short_description
        form.initial['full_description'] = event_inf.full_description
        form.initial['start_date'] = event_inf.start_date
        form.initial['end_date'] = event_inf.end_date

        return render(request, 'elists/event_update.html', {'form': form, 'event': event_inf})


def event_update_image(request, pk):
    if request.method == 'POST':
        form = UpdateImageEvent(request.POST, request.FILES)
        if form.is_valid():
            event_inf = get_object_or_404(Event, pk=pk)
            event = Event()
            event.id = event_inf.id
            event.event_name = event_inf.event_name
            event.short_description = event_inf.short_description
            event.full_description = event_inf.full_description
            event.create_date = event_inf.create_date
            event.event_creator_id = event_inf.event_creator_id
            event.image = form.files['image']
            event.is_closed = event_inf.is_closed
            event.start_date = event_inf.start_date
            event.end_date = event_inf.end_date
            event.save()
            return redirect('event_detail', pk=event.id)
    else:
        event_inf = get_object_or_404(Event, pk=pk)
        # user_name = User.objects.get(id=event_inf.event_creator_id)
        form = UpdateImageEvent()
        # form.initial['image'] = event_inf.image

        return render(request, 'elists/event_update_image.html', {'form': form, 'event': event_inf})


def event_delete(request, pk):
    event_inf = Event.objects.get(id=pk)
    event_user = EventUser.objects.filter(event_id=event_inf.id)
    if request.method == "POST":
        # event_inf = Event.objects.get(id=pk)
        # user_name = User.objects.get(id=event_inf.event_creator_id)
        # event_user = EventUser.objects.filter(event_id=event_inf.id)
        event_user.delete()
        event_inf.delete()
        return redirect('elists')
    else:
        if int(event_user[0].user_id) == int(request.user.id):
            event_inf = get_object_or_404(Event, pk=pk)
            # user_name = User.objects.get(id=event_inf.event_creator_id)
            return render(request, 'elists/event_delete.html', context={'event': event_inf, 'user_name': request.user.id})
        else:
            return redirect('elists')

