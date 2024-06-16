"""
URL configuration for stackprj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path , include
from stackusers import views as user_view
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
from stackusers.views import user_list
#from stackusers.views import signup,all_badges,user_badges
from stackbase.views import tags



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stackbase.urls')),

    #Authentication System
    path('register/' , user_view.register , name = "register" ),
    path('login/' , auth_view.LoginView.as_view(template_name="stackusers/login.html"), name='login'),
    path('logout/' , auth_view.LogoutView.as_view(template_name="stackusers/logout.html"), name='logout'),

    #Profile
    path('profile/' , user_view.profile, name="profile"),
    path('profile/update/<str:username>/' , user_view.profile_update , name='profile_update'),
    #path('signup/', signup, name='signup'),
    #users
    path('users/', user_list, name='user_list'),
    #path('badges/', all_badges, name='badge_list'),  
    #path('userbadges/<int:user_id>/', user_badges, name='user_badges'),
    path('notifications/', include('notifications_app.urls')),
    path('tags/', tags, name="tags"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
