"""my_site URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from elists import views as elists_views
# from elists.views import (
#     EventDetailView,
# UserEventListView
# )


urlpatterns = [
    path('elists/', elists_views.elists, name='elists'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('create_event/', elists_views.create_event, name='create_event'),
    path('elists/<int:pk>/', elists_views.event_detail, name='event_detail'),
    path('elists/delete_event/<int:pk>/', elists_views.event_delete, name='event_delete'),
    path('elists/update_event/<int:pk>/', elists_views.event_update, name='event_update'),
    path('elists/update_event_image/<int:pk>/', elists_views.event_update_image, name='event_update_image'),
    path('create_event_plan/<int:pk>/', elists_views.create_event_plan, name='create_event_plan'),
    path('update_event_plan/<int:pk>/', elists_views.event_update_plan, name='update_event_plan'),
    path('delete_event_plan/<int:pk>/', elists_views.event_delete_plan, name='delete_event_plan'),
    path('elists/up_priority_plan/<int:pk>/', elists_views.event_up_priority_plan, name='event_up_priority_plan'),
    path('elists/down_priority_plan/<int:pk>/', elists_views.event_down_priority_plan, name='event_down_priority_plan'),
    # path('user/<str:username>', UserEventListView.as_view(), name='user-events'),
    path('', include('blog.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
