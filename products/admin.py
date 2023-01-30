from django.contrib import admin
from products.models import Product, Comment

# Register your models here.

admin.site.register(Product)
admin.site.register(Comment)