from django.template.context_processors import request
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

class CartViewSet(viewsets.ModelViewSet):
    """В'юсет для управління кошиком"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Отримуємо кошик тільки для поточного користувача"""
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Отримання кошика поточного користувача"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        """Додає продукт у кошик або збільшує його кількість"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "Необхідно вказати product_id"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Продукт не знайдено"}, status=404)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Продукт додано", "cart_item": CartItemSerializer(cart_item).data})

    @action(detail=False, methods=['post'])
    def remove_product(self, request):
        """Видаляє продукт з кошика або зменшує його кількість"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "Необхідно вказати product_id"}, status=400)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Продукт не знайдено в кошику"}, status=404)

        if cart_item.quantity > quantity:
            cart_item.quantity -= quantity
            cart_item.save()
        else:
            cart_item.delete()

        return Response({"message": "Продукт оновлено або видалено"})

    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Очищує весь кошик"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({"message": "Кошик очищено"})
