from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    image = models.ImageField(null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    created_date = models.DateField(auto_now_add =True)
    modified_date = models.DateField(auto_now = True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    text = models.TextField()
    created_date = models.DateField(auto_now=True)
    post = models.ForeignKey(Product, on_delete = models.CASCADE)
