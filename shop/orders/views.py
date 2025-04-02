from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail
from django.conf import settings

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem

class OrderViewSet(viewsets.ModelViewSet):
    """В'юсет для управління замовленнями"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Повертає список замовлень користувача або всі замовлення для адміністратора"""
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Отримання деталей конкретного замовлення"""
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """Створює замовлення на основі кошика користувача"""
        cart_id = request.data.get("cart_id")
        try:
            cart = Cart.objects.get(id=cart_id, user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Кошик не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        if not cart.items.exists():
            return Response({"error": "Кошик порожній"}, status=status.HTTP_400_BAD_REQUEST)

        # Створення замовлення
        order = Order.objects.create(user=request.user, total_price=0)

        total_price = 0
        for cart_item in cart.items.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )
            total_price += cart_item.product.price * cart_item.quantity

        # Оновлення загальної ціни замовлення
        order.total_price = total_price
        order.save()

        # Очищення кошика після створення замовлення
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        """Оновлення статусу замовлення (тільки для адміністратора)"""
        order = self.get_object()
        new_status = request.data.get("status")

        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({"error": "Некоректний статус"}, status=400)

        order.status = new_status
        order.save()

        # Надсилання email користувачу
        subject = f"Ваше замовлення #{order.id} оновлено"
        message = f"Статус вашого замовлення #{order.id} змінено на: {new_status}.\n\nДякуємо за покупку!"
        recipient_email = order.user.email

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])

        return Response({"message": "Статус оновлено, email надіслано", "order": OrderSerializer(order).data})
