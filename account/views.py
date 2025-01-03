from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.contrib.auth import logout
from datetime import date, timedelta
from django.contrib import messages 
from django.db.models import Sum
from .decorators import *
from .filters import *
from .models import *
from .forms import *
import requests
import calendar
import json


# USERS

@login_required(login_url='login')
@admin_only_required
@login_required(login_url='login')
def homeView(request):
    context = {}
    return render(request, 'home.html', context)

@login_required(login_url='login')
@admin_only_required
def refreshUserList(request):
    usernames = User.objects.values_list('username', flat=True)
    API_Users = 'https://api.ldap.groupe-hasnaoui.com/get/users?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJUb2tlbiI6IkZvciBEU0kiLCJVc2VybmFtZSI6ImFjaG91cl9hciJ9.aMy1LUzKa6StDvQUX54pIvmjRwu85Fd88o-ldQhyWnE'
    GROUP_Users = 'https://api.ldap.groupe-hasnaoui.com/get/users/group/PUMA-PAY?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJUb2tlbiI6IkZvciBEU0kiLCJVc2VybmFtZSI6ImFjaG91cl9hciJ9.aMy1LUzKa6StDvQUX54pIvmjRwu85Fd88o-ldQhyWnE'
    response = requests.get(API_Users)
    response_ = requests.get(GROUP_Users)
    if response.status_code == 200 and response_.status_code == 200:
        data = json.loads(response.content)
        group_users = json.loads(response_.content)['members']
        new_users_list = [user for user in data['users'] if user['fullname'] in group_users and user['AD2000'] not in usernames]
        for user in new_users_list:
            user = User(username= user['AD2000'], password='password', fullname=user['fullname'], role='Nouveau', is_admin=False, first_name= user['fname'], email= user['mail'], last_name = user['lname'])
            user.save()
    else:
        print('Erreur : could not fetch data from API.')
    cache_param = str(uuid.uuid4())
    url_path = reverse('users')
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)


@login_required(login_url='login')
@admin_only_required
def editUserView(request, id):
    user = User.objects.get(id=id)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save(user=request.user)
            form.save_m2m()
            return redirect(getRedirectionURL(request, url_path = reverse('users')))
    context = {'form': form, 'user_': user }
    return render(request, 'user_form.html', context)

@login_required(login_url='login')
@admin_only_required
def deleteUserView(request, id):
    user = get_object_or_404(User, id=id)
    try:
        user.delete()
        url_path = reverse('users')
        return redirect(getRedirectionURL(request, url_path))
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression d'utilisateur: {e}")
        return redirect(getRedirectionURL(request, reverse('users')))

@login_required(login_url='login')
@admin_only_required
def listUserView(request):
    users = User.objects.exclude(username='admin').order_by('-date_modified')
    filteredData = UserFilter(request.GET, queryset=users)
    users = filteredData.qs
    paginator = Paginator(users, request.GET.get('page_size', 12))
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'filteredData': filteredData}
    return render(request, 'list_users.html', context)

# AUTHENTIFICATION

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

def logoutView(request):
    logout(request)
    return redirect('login')

