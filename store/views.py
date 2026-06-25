from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Product, Category, ProductReview
from orders.models import Cart, CartItem


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def home(request):
    featured = Product.objects.filter(is_featured=True, is_available=True)[:8]
    categories = Category.objects.all()[:6]
    new_arrivals = Product.objects.filter(is_available=True)[:8]
    return render(request, 'store/home.html', {
        'featured': featured,
        'categories': categories,
        'new_arrivals': new_arrivals,
    })


def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    query = request.GET.get('q')
    sort = request.GET.get('sort', 'newest')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        category = None

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort_map = {
        'newest': '-created_at',
        'price_low': 'price',
        'price_high': '-price',
        'name': 'name',
    }
    products = products.order_by(sort_map.get(sort, '-created_at'))

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'active_category': category,
        'query': query,
        'sort': sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    reviews = product.reviews.all().order_by('-created_at')
    related = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        if 'review_submit' in request.POST:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            if rating and comment:
                ProductReview.objects.update_or_create(
                    product=product, user=request.user,
                    defaults={'rating': rating, 'comment': comment}
                )
                messages.success(request, 'Review submitted!')
                return redirect('store:product_detail', slug=slug)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related': related,
        'avg_rating': avg_rating,
        'user_review': user_review,
    })


def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()
    messages.success(request, f'"{product.name}" added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'store:cart'))


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    return redirect('store:cart')


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('store:cart')


def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_available=True
    ) if query else Product.objects.none()
    return render(request, 'store/search_results.html', {'products': products, 'query': query})
