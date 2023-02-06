from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from templates.users.forms import AuthForm, RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.views.generic import ListView, RedirectView, CreateView
# Create your views here.

class AuthView(ListView):
    def auth_view(self, request, **kwargs):
            context = {
                'form' : AuthForm
            }
            return render(request,self.template_name, context=context)
    def auth_post_view(self, request, *args, **kwargs):
            form = AuthForm(data=request.POST)

            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data.get("username"),
                    password = form.cleaned_data.get("password")
                )
                if user:
                    login(request,user)
                    return redirect('/products')
                else:
                    form.add_error('username','одной буквы не хватает')
            return render(request, 'users/auth.html',context={
                'form' : form
            })

class LogOutView(RedirectView, CreateView):
    def logout_view(self, request, *args, **kwargs):
        logout(request)
        return redirect('/products/')
class RegisterView(ListView,CreateView):
    def register_view(self, request, *args, **kwargs):
                context={
                    'form': RegisterForm
                }
                return render(request, "users/register.html",context = context)

    def register_post_view(selfself, request, *args, **kwargs):
                form = RegisterForm(data=request.POST)
                if form.is_valid():
                    password1, password2 = form.cleaned_data.get('password1'),form.cleaned_data.get('password2')
                    if password1 == password2:
                        User.objects.create_user(
                            username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password1')
                        )
                        return redirect('/users/login/')
                    else:
                        form.add_error('password1', 'по моему ты что-то напутал')
                return render(request, 'users/register.html',context = {
                    'form': form
                })
