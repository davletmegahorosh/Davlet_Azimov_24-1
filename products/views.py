from django.shortcuts import render,redirect
# from datetime import datetime
from products.models import Product, Comment
from templates.products.forms import ProductCreateForm,CommentCreateForm
from django.views.generic import ListView, CreateView, DetailView, View

PAGINATION_LIMIT = 3
class MainView(ListView):
    pass
class ProductSView(ListView):
    def get(self,request, **kwargs):
        products = self.get_queryset()
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if search is not None:
            products = Product.objects.filter(
                title__icontains=search
                # comment__author__isnull = False
            )

        maxpage = products.__len__() / PAGINATION_LIMIT
        if round(maxpage) < maxpage:
            maxpage = round(maxpage) + 1
        else:
            maxpage = round(maxpage)

        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        context = {
            'products': products,
            'user': request.user,
            'maxpage': range(1, maxpage + 1),
        }
        return render(request, self.template_name, context=context)

class ProductDetailView(DetailView):
    pk_url_kwarg = 'id'
    def product_detail_view(self, request, id):
            product_obj = Product.objects.get(id=id)
            comments = Comment.objects.filter(post=product_obj)
            context = {
                'post': product_obj,
                'comments': comments,
                'form': CommentCreateForm
            }
            return render(request, self.template_name, context=context)
    def CreateCommentView(self, request, id):
            product_obj = Product.objects.get(id=id)
            comments = Comment.objects.filter(post=product_obj)
            form = CommentCreateForm(data=request.POST)
            if form.is_valid():
                Comment.objects.create(
                    post=product_obj,
                    text = form.cleaned_data.get('text')
                )
                return redirect(f'/products/{product_obj.id}')
            return render(request, "products/detail.html", context={
                'product' : product_obj,
                'comments' :comments,
                'form': form
            })

class CreateProductView(ListView, CreateView):
    form = ProductCreateForm
    def create_product(self, request, **kwargs):
        if not request.user.is_anonymous:
            context = {
                'form' :ProductCreateForm
            }
            return render(request, 'products/create.html',context=context)
        elif request.user.is_anonymous:
            return redirect('/products')
    def create_products(self, request, **kwargs):
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            Product.objects.create(
                title = form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data['price'] if form.cleaned_data['price'] is not None else 5
            )
            return redirect('/products/')
        return render(request, "products/create.html" ,context={
            'form' : form
        })