from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ToDoItem(models.Model):
    title = models.CharField(max_length=255)
    description =models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')

    def __str__(self):
        return self.title