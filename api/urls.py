from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('tasks/', TaskView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskView.as_view(), name='task-detail'),
    path('google/', google_auth, name='google-auth')
]