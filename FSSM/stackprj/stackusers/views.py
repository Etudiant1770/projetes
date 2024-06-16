from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .forms import UserSearchForm
from .models import User,Profile
from django.contrib.auth import login
from channels.layers import get_channel_layer
import json
from django.shortcuts import  HttpResponse
from django.contrib.auth.models import User



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request , f'Account successfully created for {username}! Login In Now')
            return redirect('stackbase:home')
    else: 
        form = UserRegisterForm()

    return render(request , 'stackusers/register.html' , {'form' : form})


@login_required
def profile(request):
    #user_badges = UserBadge.objects.filter(user=request.user)
    return render(request, 'stackusers/profile.html')
#########################################################

@login_required
def profile_update(request,username):
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Acount Updated Successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'stackusers/profile_update.html', context)
#page users
def user_list(request):
    if request.method == 'GET':
        form = UserSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # Effectuer la recherche d'utilisateurs
            users = User.objects.filter(username__icontains=search_query)
        else:
            users = User.objects.all()
    else:
        users = User.objects.all()
    
    context = {
        'all_users': users,
        'form': form,
    }
    return render(request, 'user_list.html', context)




 # def user_badges(request, user_id):
  #    user_badges = UserBadge.objects.filter(user_id=user_id)
   #   return render(request, 'user_badges.html', {'user_badges': user_badges})

 # def all_badges(request):
   #   badges = Badge.objects.all()
    #  return render(request, 'all_badges.html', {'badges': badges})


 # def signup(request):
     # if request.method == 'POST':
     #     form = UserCreationForm(request.POST)
        #  if form.is_valid():
         #     user = form.save()
          #    login(request, user)
            #  return redirect('home')  # Remplacez 'home' par le nom de la vue vers laquelle vous souhaitez rediriger après l'inscription
     # else:
        #  form = UserCreationForm()
     # return render(request, 'stackusers/signup.html', {'form': form})
from django.template import RequestContext
def home(request):
    return render(request, 'mainapp/index.html', {
        'room_name': "broadcast"
    })

from asgiref.sync import async_to_sync
def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps("Notification")
        }
    )
    return HttpResponse("Done")