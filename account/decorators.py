from django.template.defaulttags import register
from django.shortcuts import render, redirect
import uuid

# DECORATORS

@register.filter
def startwith(value, word):
    return str(value).startswith(word)

@register.filter
def is_login(messages):
    for message in messages:
        if str(message).startswith('LOGIN'):
            return True
    return False

@register.filter
def loginerror(value, word):
    return str(value)[len(word):]

def login_success(request):
    user = request.user
    if user.has_admin() or user.has_commercial() or user.has_backoffice():
        return redirect("tasks")
    elif user.has_admin():
        return redirect("home")
    return redirect("home")

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin' or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return wrapper

def admin_only_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin':
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return wrapper

def page_not_found(request, exception):
    return render(request, '404.html', status=404)

# REDIRECTION
def getRedirectionURL(request, url_path):
    params = {
        'page': request.GET.get('page', '1'),
        'page_size': request.GET.get('page_size', '12'),
        'search': request.GET.get('search', ''),
        'state': request.GET.get('state', ''),
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'zone': request.GET.get('zone', ''),
        'new_users_only': request.GET.get('new_users_only', ''),
        'payment_type': request.GET.get('payment_type', '')
    }
    cache_param = str(uuid.uuid4())
    query_string = '&'.join([f'{key}={value}' for key, value in params.items() if value])
    return f'{url_path}?cache={cache_param}&{query_string}'
