from django.db import models
from django.contrib.auth.models import User
# Create your models here. 1. models reperesents tables , model  is a class 
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self)->str:
        return self.name
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    categorys = models.ForeignKey(Category, on_delete=models.CASCADE)

class Student(models.Model):
    name=models.CharField(max_length=50)
    uid=models.IntegerField(null=True, blank=True)
    mobile=models.IntegerField(null=True, blank=True)
    course=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    date_of_birth=models.DateField(null=True, blank=True)
    gender=models.CharField(max_length=50)
    address=models.CharField(max_length=250)
    college_name=models.CharField(max_length=50)
    district=models.CharField(max_length=50)