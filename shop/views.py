from decimal import Decimal

from django.contrib import messages
from django.db.models import Case, IntegerField, When
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Product
from .seed import seed_clothes_catalog


def _cart_details(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0.00")
    count = 0
    for product_id, qty in list(cart.items()):
        try:
            product = Product.objects.get(pk=int(product_id))
        except (Product.DoesNotExist, ValueError, TypeError):
            continue
        qty = int(qty)
        price = product.price or Decimal("0.00")
        subtotal = price * qty
        items.append({"product": product, "qty": qty, "subtotal": subtotal})
        total += subtotal
        count += qty
    return items, total, count


def home(request):
    seed_clothes_catalog()

    if request.method == "POST":
        action = request.POST.get("action")
        cart = request.session.get("cart", {})

        if action == "add":
            product = get_object_or_404(Product, pk=request.POST.get("product_id"))
            key = str(product.id)
            cart[key] = int(cart.get(key, 0)) + 1
            request.session["cart"] = cart
            messages.success(request, f"{product.name} added to cart.")
            return redirect("/#products")

        if action == "remove":
            cart.pop(str(request.POST.get("product_id")), None)
            request.session["cart"] = cart
            messages.success(request, "Item removed from cart.")
            return redirect("/#cart")

        if action == "checkout":
            if not cart:
                messages.error(request, "Your cart is empty.")
                return redirect("/#checkout")
            name = request.POST.get("name", "").strip()
            address = request.POST.get("address", "").strip()
            if not name or not address:
                messages.error(request, "Please enter your name and address.")
                return redirect("/#checkout")
            request.session["cart"] = {}
            messages.success(request, f"Thanks {name}! Your order has been placed.")
            return redirect("/#checkout")

        return redirect("/")

    category_order = Case(
        When(name="Men", then=0),
        When(name="Women", then=1),
        When(name="Children", then=2),
        default=3,
        output_field=IntegerField(),
    )
    categories = (
        Category.objects.filter(name__in=["Men", "Women", "Children"])
        .annotate(sort=category_order)
        .order_by("sort")
    )
    products = (
        Product.objects.filter(category__in=categories)
        .select_related("category")
        .annotate(sort=Case(
            When(category__name="Men", then=0),
            When(category__name="Women", then=1),
            When(category__name="Children", then=2),
            default=3,
            output_field=IntegerField(),
        ))
        .order_by("sort", "name")
    )
    items, total, count = _cart_details(request)
    return render(
        request,
        "shop/home.html",
        {
            "categories": categories,
            "products": products,
            "cart_items": items,
            "cart_total": total,
            "cart_count": count,
        },
    )
