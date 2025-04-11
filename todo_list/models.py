from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ToDoList(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title