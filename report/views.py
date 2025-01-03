from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .filters import *
from django.core.paginator import Paginator
import uuid
from django.urls import reverse
from functools import wraps
from django.contrib import messages
from django.http import JsonResponse
from .utils import *
from django.forms import modelformset_factory
from .utils import connect_odoo

# db, uid, models, password = connect_odoo()

# DECORATORS

def check_creator(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'id' in kwargs:
            task_id = kwargs['id']
        elif 'pk' in kwargs:
            task_id = kwargs['pk']
        task = Task.objects.get(id=task_id)
        if task.creator != request.user and request.user.role != 'Admin':
            return render(request, '403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

def resp_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Résponsable'] or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return wrapper

def direc_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Directeur'] or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return wrapper

def comm_app_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Directeur', 'Résponsable', 'Commercial'] or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return wrapper


# TASKS

@login_required(login_url='login')
@comm_app_required 
def listTaskView(request):
    tasks = Task.objects.all().order_by('-date_modified')
    filteredData = TaskFilter(request.GET, queryset=tasks)
    tasks = filteredData.qs
    page_size_param = request.GET.get('page_size')
    page_size = int(page_size_param) if page_size_param else 12   
    paginator = Paginator(tasks, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = { 'page': page, 'filtredData': filteredData }
    return render(request, 'list_tasks.html', context)

@login_required(login_url='login')
@check_creator
def deleteTaskView(request, id):
    task = get_object_or_404(User, id=id)
    try:
        task.delete()
        url_path = reverse('tasks')
        return redirect(getRedirectionURL(request, url_path))
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression de la tâche: {e}")
        return redirect(getRedirectionURL(request, reverse('tasks')))

@login_required(login_url='login')
@comm_app_required
def createTaskView(request):
    form = TaskForm(user=request.user)
    ImageFormSet = modelformset_factory(Image,form=ImageForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if form.is_valid() and formset.is_valid():
            task = form.save(commit=False)
            task.state = 'A Faire'
            task.save()
            for image in formset:
                if image.cleaned_data.get('DELETE'):
                    if image.instance.pk:
                        image.instance.delete()
                else:
                    if image.instance.pk is None:
                        image.instance.task = task
                    if image.instance.image:
                        image.save() 
            return redirect(getRedirectionURL(request, reverse('tasks')))
        else:
            print("Form Errors:", form.errors)
            print("Formset Errors:")
            for subform in formset:
                print(subform.errors)
    else:
        formset = ImageFormSet(queryset=Image.objects.none())
    context = {'form': form, 'formset': formset }
    return render(request, 'task_form.html', context)

@login_required(login_url='login')
@check_creator
def editTaskView(request, id):
    task = Task.objects.get(id=id)
    form = TaskForm(instance=task, user=request.user)
    ImageFormSet = modelformset_factory(Image,form=ImageForm, extra=0, can_delete=True)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task, user=request.user)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.filter(task=task))
        if form.is_valid() and formset.is_valid():
            task = form.save(commit=False)
            task.save()
            for image in formset:
                if image.cleaned_data.get('DELETE'):
                    if image.instance.pk:
                        image.instance.delete()
                else:
                    if image.instance.pk is None:
                        image.instance.task = task
                    if image.instance.image:
                        image.save() 
            return redirect(getRedirectionURL(request, reverse('detail_task', args=[task.id])))
    else:
        formset = ImageFormSet(queryset=Image.objects.filter(task=task))
    context = {'form': form, 'task': task, 'formset': formset }
    return render(request, 'task_form.html', context)

@login_required(login_url='login')
@check_creator
def doneTask(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        messages.success(request, 'Tâche n\'existe pas')

    url_path = reverse('detail_task', args=[task.id])
    if task.state == 'Fait':
        return redirect(getRedirectionURL(request, url_path))
    
    task.state = 'Fait'
    task.save()
    messages.success(request, 'Tâche marquée comme fait')
    return redirect(getRedirectionURL(request, url_path))

@login_required(login_url='login')
@check_creator
def draftTask(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        messages.success(request, 'Tâche n\'existe pas')

    url_path = reverse('detail_task', args=[task.id])
    if task.state == 'A Faire':
        return redirect(getRedirectionURL(request, url_path))
    
    task.state = 'A Faire'
    task.save()
    messages.success(request, 'Tâche marquée comme a faire')
    return redirect(getRedirectionURL(request, url_path))

@login_required(login_url='login')
@comm_app_required
def detailTaskView(request, id):
    task = Task.objects.get(id=id)
    context = {'task': task }
    return render(request, 'task_detail.html', context)

@login_required(login_url='login')
def live_search(request):

    search_for = request.GET.get('search_for', '')
    term = request.GET.get('search_term', '')

    if search_for == 'client':
        domain = [['name', 'ilike', term], '|', '|',['customer', '=', True], ['is_company', '=', True]]
    else:
        domain = [['name', 'ilike', term]]

    fields = ['id', 'name']

    search_for_mapping = {
        'comm_team': ['crm.case.section', domain, fields],
        'task_type': ['crm.task.type', domain, fields],
        'project': ['crm.project', domain, fields],
        'lead': ['crm.lead', domain, fields],
        'client': ['res.partner', domain, fields],
        'wilaya': ['res.country.state', domain, fields]
    }

    model = search_for_mapping.get(search_for)

    if model:
        results = models.execute_kw(db, uid, password, model[0], 'search_read', [model[1]], {'fields': model[2], 'limit': 10})
        data = [{'id': obj['id'], 'name': obj['name']} for obj in results]
    else:
        data = []

    return JsonResponse(data, safe=False)


def getRedirectionURL(request, url_path):
    params = {
        'page': request.GET.get('page', '1'),
        'page_size': request.GET.get('page_size', '12'),
        'search': request.GET.get('search', ''),
        'state': request.GET.get('state', ''),
    }
    cache_param = str(uuid.uuid4())
    query_string = '&'.join([f'{key}={value}' for key, value in params.items() if value])
    return f'{url_path}?cache={cache_param}&{query_string}'