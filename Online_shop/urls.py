"""Blog1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from products.models import Product
from products.views import ProductDetailView,CreateView,MainView, ProductSView
from Online_shop.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from users.views import AuthView, LogOutView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(model = Product,template_name = 'layouts/index.html')),
    path('products/',ProductSView.as_view(template_name='products/posts.html',model=Product)),
    path('products/<int:id>/',ProductDetailView.as_view(model=Product,template_name='products/detail.html')),
    path('products/create/',CreateView.as_view(model=Product, template_name='products/posts.html')),

    path('users/login',AuthView.as_view(template_name = 'users/auth.html')),
    path('users/logout',LogOutView.as_view()),
    path('users/register/',RegisterView.as_view(template_name = 'users/register.html')),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)