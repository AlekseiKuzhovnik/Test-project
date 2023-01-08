from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Weather
import requests
from datetime import datetime


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'О ресурсе "Make your event"'})


def weather():
    api_key = '59deedba5f4178b4168ab7f6d038454f'
    city = 'Wroclaw'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'

    today = datetime.now()

    select_result = Weather.objects.filter(city=city, last_update__day=int(today.strftime("%d")), last_update__hour=int(today.strftime("%H")))
    # for i in select_result:
    #     print(i.last_update)
    if select_result:
        symbol = '+' if list(select_result)[0].degree > 0 else ''
        res = {
            'city': list(select_result)[0].city,
            'temp': symbol + str(list(select_result)[0].degree),
            'icon': list(select_result)[0].icon_name
        }
    else:
        res = requests.get(url).json()
        symbol = '+' if round(res["main"]["temp"]) > 0 else ''
        res = {
            'city': city,
            'temp': symbol + str(round(res["main"]["temp"])),
            'icon': res["weather"][0]["icon"]
        }
        new_record = Weather(city=res['city'], degree=res["temp"], icon_name=res["icon"])
        new_record.save()

    context = {
        'info': res
    }

    return context
