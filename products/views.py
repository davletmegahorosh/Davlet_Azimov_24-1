from django.shortcuts import render,redirect
# from datetime import datetime
from products.models import Product, Comment
from templates.products.forms import ProductCreateForm,CommentCreateForm

PAGINATION_LIMIT = 2

def main(request):
    if request.method =='GET':
        return render(request,'layouts/index.html')

def products_views(request):
    if request.method == 'GET':
        products = Product.objects.all()
        search = request.GET.get('search')
        page = int(request.GET.get('page',1))
        context = {
            'products': products,
            'user': request.user}
        if search is not None:
            product = Product.objects.filter(
                description__icontains = search
                # comment__author__isnull = False
            )

        maxpage= products.__len__() / PAGINATION_LIMIT
        if round(maxpage) > maxpage:
            maxpage = round(maxpage) +1
        else:
            maxpage = round(maxpage)

        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        context = {
            'products': products,
            'user': request.user,
            'maxpage' : range(1,maxpage+1),
            }
        return render(request, "products/posts.html", context=context )
def product_detail_view(request, id):
    if request.method == 'GET':
        product_obj = Product.objects.get(id=id)
        comments = Comment.objects.filter(post=product_obj)
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
        return redirect('/products')
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