from django.urls import path
from .views import RegisterView, LoginView, ToDoItemCreateView, ToDoItemUpdateView, ToDoItemDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('todos/create/', ToDoItemCreateView.as_view(), name='todo-create'),
    path('todos/update/<int:pk>', ToDoItemUpdateView.as_view(), name='todo-update'),
    path('todos/delete/<int:pk>', ToDoItemDeleteView.as_view(), name='todo-delete'),
]