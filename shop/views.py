from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.db.models import Min,Max,Count
from .models import *
from .forms import SignupForm,ReviewAdd
from django.contrib.auth import login,authenticate

# Домашняя страница
def home(request):
    banners = Banneer.objects.all().order_by('-id')
    data = Product.objects.filter(is_featured=True).order_by('id')
    return render(request, 'index.html', {'data': data, 'banners': banners})

#Категории
def category_list(request):
    data = Category.objects.all().order_by('-id')
    return render(request, 'category_list.html', {'data': data})

#Бренды
def brand_list(request):
    data = Brand.objects.all().order_by('-id')
    return render(request, 'brand_list.html', {'data': data})

#Список товаров
def product_list(request):
    total_data=Product.objects.count()
    data = Product.objects.all().order_by('-id')[:3]
    min_price=ProductAttribute.objects.aggregate(Min('price'))
    max_price = ProductAttribute.objects.aggregate(Max('price'))
    return render(request, 'product_list.html',
        {
            'data': data,
            'total_data':total_data,
            'min_price':min_price,
            'max_price': max_price,
        }
        )

#Список товаров по категориям
def category_product_list(request,cat_id):
    category=Category.objects.get(id=cat_id)
    data=Product.objects.filter(category=category).order_by('-id')
    return render(request, 'category_product_list.html', {
            'data': data,
            })

#Список товаров по брендам
def brand_product_list(request,brand_id):
    brand=Brand.objects.get(id=brand_id)
    data=Product.objects.filter(brand=brand).order_by('-id')
    return render(request, 'brand_product_list.html', {
            'data': data,
            })

# Детали товара
def product_detail(request, slug, id):
    product=Product.objects.get(id=id)
    related_produtcs = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    sizes = ProductAttribute.objects.filter(product=product).values('size__id','size__title','price').distinct()
    reviewForm=ReviewAdd()

    #Проверка на добавление отзыва
    canAdd=True
    reviewCheck=ProductReview.objects.filter(user=request.user, product=product).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd=False

    return render(request, 'product_detail.html', {'data':product, 'related':related_produtcs,'sizes':sizes, 'reviewForm': reviewForm, 'canAdd': canAdd})

# Функция Поиска
def search(request):
    q=request.GET['q']
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request, 'search.html', {'data': data})

# Данные фильтра
def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)
    if len(categories)>0:
        allProducts=allProducts.filter(category__id__in=categories).distinct()
    if len(brands)>0:
        allProducts=allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes)>0:
        allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t = render_to_string('ajax/product-list.html', {'data':allProducts})
    return JsonResponse(({'data':t}))

# Показать больше
def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset+limit]
    t = render_to_string('ajax/product-list.html', {'data': data})
    return JsonResponse(({'data': t}))

# Добавление в корзину
def add_to_cart(request):
    #del request.session['cartdata']
    cart_p={}
    cart_p[str(request.GET['id'])]={
        'image': request.GET['image'],
        'title':request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata']=cart_p
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})


# Корзина
def cart_list(request):
    total_amt=0
    for p_id, item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    return render(request, 'cart.html', {'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})

# Удаление из корзины
def delete_cart_item(request):
    p_id=str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata']=cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty']) * float(item['price'])
    t = render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data': t,'totalitems':len(request.session['cartdata'])})

# Обновление корзины
def update_cart_item(request):
    p_id=str(request.GET['id'])
    p_qty=request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=p_qty
            request.session['cartdata']=cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty']) * float(item['price'])
    t = render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data': t,'totalitems':len(request.session['cartdata'])})

# Регистрация
def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=pwd)
            login(request,user)
            return redirect('home')
    form=SignupForm
    return render(request, 'registration/signup.html', {'form': form})

#Сохранение отзыва
def save_review(request,pid):
    product=Product.objects.get(pk=pid)
    user=request.user
    review=ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
        )
    return JsonResponse({'bool':True})
