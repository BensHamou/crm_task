from django.urls import path
from .views import *


urlpatterns = [

    path('task/all/', listTaskView, name='tasks'),
    path('', listTaskView, name='tasks'),
    path('task/create/', createTaskView, name='create_task'),
    path('task/edit/<int:id>/', editTaskView, name='edit_task'),
    path('task/delete/<int:id>/', deleteTaskView, name='delete_task'),
    path('task/<int:id>/detail/', detailTaskView, name='detail_task'),
    
    path('task/<int:id>/done/', doneTask, name='done_task'),
    path('task/<int:id>/draft/', draftTask, name='draft_task'),
    
    path('live_search/', live_search, name='live_search'),

]

