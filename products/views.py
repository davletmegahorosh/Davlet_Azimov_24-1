from django.shortcuts import render,redirect
# from datetime import datetime
from products.models import Product, Comment
from templates.products.forms import ProductCreateForm,CommentCreateForm

def main(request):
    if request.method =='GET':
        return render(request,'layouts/index.html')

def products_views(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, "products/posts.html", context={
            'products': products,
            'user': request.user
        })
def product_detail_view(request, id):
    if request.method == 'GET':
        product_obj = Product.objects.get(id=id)
        comments = Comment.objects.filter(prouct=product_obj)
        context = {
            'post': product_obj,
            'comments': comments,
            'form': CommentCreateForm
        }
        return render(request, "products/detail.html", context=context)
    if request.method =='POST':
        product_obj = Product.objects.get(id=id)
        comments = Comment.objects.filter(product=product_obj)
        form = CommentCreateForm(data=request.POST)
        if form.is_valid():
            Comment.objects.create(
                product=product_obj,
                text = form.cleaned_data.get('text')
            )
            return redirect(f'/posts/{id}/')
        return render(request, "products/detail.html", context={
            'post' : product_obj,
            'comments' :comments,
            'form': form
        })

def create_product(request):
    if request.method == 'GET'and not request.user.is_anonymous:
        context = {
            'form' :ProductCreateForm
        }
        return render(request, 'products/create.html',context=context)
    elif request.user.is_anonymous:
        return redirect('/posts')
    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)

        if form.is_valid():
            Product.objects.create(
                title = form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data['price'] if form.cleaned_data['price'] is not None else 5
            )
            return redirect('/products/')
        return render(request, "products/detail.html" ,context={
            'form' : form
        })