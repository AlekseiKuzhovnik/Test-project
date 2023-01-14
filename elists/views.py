from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventUser, EventPlan
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from .forms import CreateEvent, UpdateEvent, UpdateImageEvent, CreateEventPlan
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
    if not request.user.id:
        return redirect('login')
    elif int(event_inf.event_creator_id) == int(request.user.id):
        event_inf = get_object_or_404(Event, pk=pk)
        user_name = User.objects.get(id=event_inf.event_creator_id)
        plan = EventPlan.objects.raw("SELECT * FROM elists_eventplan where event_id = %s order by priority", [pk])
        # max_priority = EventPlan.objects.raw("SELECT max(priority) as max_priority FROM elists_eventplan where event_id = %s", [pk])
        # max_priority = EventPlan.objects.latest('priority').priority
        max_priority = EventPlan.objects.filter(event_id=pk).order_by('-priority').first()
        max_priority = max_priority.priority if max_priority else 0
        return render(request, 'elists/event_detail.html', context={'event': event_inf, 'user_name': user_name, 'plan': plan, 'max_priority': max_priority})
    else:
        return redirect('elists')


def event_update(request, pk):
    event_inf = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = UpdateEvent(request.POST)
        if form.is_valid():
            print(f"------------------>>{event_inf.id}")
            event = Event()
            event.id = pk
            event.event_name = form.cleaned_data['event_name']
            event.short_description = form.cleaned_data['short_description']
            event.full_description = form.cleaned_data['full_description']
            event.create_date = event_inf.create_date
            event.event_creator_id = event_inf.event_creator_id
            event.image = event_inf.image
            event.is_closed = event_inf.is_closed
            event.start_date = form.cleaned_data['start_date']
            event.end_date = form.cleaned_data['end_date']
            event.save()
            return redirect('event_detail', pk=pk)
        else:
            return render(request, 'elists/event_update.html', {'form': form, 'event': event_inf})
    else:
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
        print(f"------------------------->>>>>{form.files['image']}")
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
        form = UpdateImageEvent()

        return render(request, 'elists/event_update_image.html', {'form': form, 'event': event_inf})


def event_delete(request, pk):
    event_inf = Event.objects.get(id=pk)
    event_user = EventUser.objects.filter(event_id=event_inf.id)
    if request.method == "POST":
        event_plan = EventPlan.objects.filter(event_id=pk)
        # user_name = User.objects.get(id=event_inf.event_creator_id)
        # event_user = EventUser.objects.filter(event_id=event_inf.id)
        event_plan.delete()
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


def create_event_plan(request, pk):
    if request.method == "POST":
        form = CreateEventPlan(request.POST)
        if form.is_valid():
            plan = EventPlan()
            plan.event_id = pk
            plan.plan_name = form.cleaned_data['plan_name']
            plan.plan_short_description = form.cleaned_data['plan_short_description']
            plan.plan_full_description = form.cleaned_data['plan_full_description']
            plan.create_date = datetime.now()
            plan.start_date = form.cleaned_data['start_date']
            plan.end_date = form.cleaned_data['end_date']

            pr = EventPlan.objects.filter(event_id=pk).order_by('-priority').first()
            plan.priority = pr.priority + 1 if pr else 0

            plan.save()
            return redirect('event_detail', pk=pk)
    else:
        pr = EventPlan.objects.filter(event_id=33).order_by('-priority').first()
        if pr:
            print(pr)
        form = CreateEventPlan()
    return render(request, 'elists/create_event_plan.html', {'form': form})


def event_update_plan(request, pk):
    plan_inf = get_object_or_404(EventPlan, id=pk)
    if request.method == 'POST':
        form = CreateEventPlan(request.POST)
        if form.is_valid():
            plan = EventPlan()
            plan.id = pk
            plan.plan_name = form.cleaned_data['plan_name']
            plan.plan_short_description = form.cleaned_data['plan_short_description']
            plan.plan_full_description = form.cleaned_data['plan_full_description']
            plan.create_date = plan_inf.create_date
            plan.start_date = form.cleaned_data['start_date']
            plan.end_date = form.cleaned_data['end_date']
            plan.event_id = plan_inf.event_id
            plan.priority = plan_inf.priority
            plan.save()
            return redirect('event_detail', pk=plan_inf.event_id)
    else:
        # user_name = User.objects.get(id=event_inf.event_creator_id)
        form = CreateEventPlan()
        form.initial['plan_name'] = plan_inf.plan_name
        form.initial['plan_short_description'] = plan_inf.plan_short_description
        form.initial['plan_full_description'] = plan_inf.plan_full_description
        form.initial['start_date'] = plan_inf.start_date
        form.initial['end_date'] = plan_inf.end_date

        return render(request, 'elists/update_event_plan.html', {'form': form, 'plan': plan_inf})


def event_delete_plan(request, pk):
    plan_inf = EventPlan.objects.get(id=pk)
    event_user = EventUser.objects.filter(event_id=plan_inf.event_id)
    if request.method == "POST":
        event_id = plan_inf.event_id
        plan_inf.delete()
        return redirect('event_detail', pk=event_id)
    else:
        event_users = [int(event_user[i].user_id) for i in range(len(event_user))]
        if request.user.id in event_users:
            plan_inf = get_object_or_404(EventPlan, pk=pk)
            return render(request, 'elists/delete_event_plan.html', context={'plan': plan_inf, 'user_name': request.user.id})
        else:
            return redirect('elists')


def event_up_priority_plan(request, pk):
    plan_a = EventPlan.objects.get(id=pk)
    plan_b = EventPlan.objects.get(event_id=plan_a.event_id, priority=plan_a.priority-1)
    plan_a.priority, plan_b.priority = plan_b.priority, plan_a.priority
    print(f"adasdasdasdssd{plan_a.event_id}")
    plan_a.save()
    plan_b.save()
    return redirect('event_detail', pk=plan_a.event_id)


def event_down_priority_plan(request, pk):
    plan_a = EventPlan.objects.get(id=pk)
    plan_b = EventPlan.objects.get(event_id=plan_a.event_id, priority=plan_a.priority+1)
    plan_a.priority, plan_b.priority = plan_b.priority, plan_a.priority
    plan_a.save()
    plan_b.save()
    return redirect('event_detail', pk=plan_a.event_id)
