from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem

CART_SESSION_KEY = 'cart'

def _get_cart(session):
    return session.get(CART_SESSION_KEY, {})

def _save_cart(session, cart):
    session[CART_SESSION_KEY] = cart
    session.modified = True

def home(request):
    categories = Category.objects.all().order_by('name')
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:12]
    return render(request, 'store/home.html', {'categories': categories, 'products': products})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    return render(request, 'store/category.html', {'category': category, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/product_detail.html', {'product': product})

def cart_view(request):
    cart = _get_cart(request.session)
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    items = []
    total = 0
    for p in products:
        qty = cart.get(str(p.id), 0)
        subtotal = p.price * qty
        items.append({'product': p, 'quantity': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'store/cart.html', {'items': items, 'total': total})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_cart(request.session)
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    _save_cart(request.session, cart)
    messages.success(request, f'Added {product.name} to cart.')
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))

def update_cart(request, product_id):
    qty = int(request.POST.get('quantity', 1))
    cart = _get_cart(request.session)
    if qty <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = qty
    _save_cart(request.session, cart)
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = _get_cart(request.session)
    cart.pop(str(product_id), None)
    _save_cart(request.session, cart)
    return redirect('cart')

def checkout(request):
    cart = _get_cart(request.session)
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('home')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not all([full_name, email, address, city, phone]):
            messages.error(request, "Please fill in all fields.")
            return redirect('checkout')

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name, email=email, address=address, city=city, phone=phone
        )

        product_ids = [int(pid) for pid in cart.keys()]
        products = Product.objects.filter(id__in=product_ids)

        for p in products:
            qty = cart[str(p.id)]
            OrderItem.objects.create(order=order, product=p, quantity=qty, price=p.price)
            if p.stock >= qty:
                p.stock -= qty
                p.save(update_fields=['stock'])

        _save_cart(request.session, {})
        messages.success(request, "Order placed successfully!")
        return redirect('order_success', order_id=order.id)

    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    items = []
    total = 0
    for p in products:
        qty = cart[str(p.id)]
        subtotal = p.price * qty
        items.append({'product': p, 'quantity': qty, 'subtotal': subtotal})
        total += subtotal

    # Pre-fill if logged in
    initial = {}
    if request.user.is_authenticated:
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }

    return render(request, 'store/checkout.html', {'items': items, 'total': total, 'initial': initial})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})
