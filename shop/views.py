from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Category, Product, Cart, CartItem, OrderItem
from shop.serializers import CategorySerializer, ProductSerializer, CartSerializer, AddToCartSerializer, \
    CreateOrderSerializer
from .models import Order
from .serializers import OrderSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"


class CartView(RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        try:
            return Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        if cart is None:
            return Response({"detail": "Cart not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)



class AddToCartView(APIView):
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data["user_id"]
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user_id=user_id)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)



class CreateOrderView(APIView):
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data["user_id"]
        shipping_address = serializer.validated_data["shipping_address"]
        phone_number = serializer.validated_data["phone_number"]

        # get cart for this user
        try:
            cart = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found for this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_amount = cart.get_total_price()

        order = Order.objects.create(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=shipping_address,
            phone_number=phone_number,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Order.objects.filter(user_id=user_id)


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer