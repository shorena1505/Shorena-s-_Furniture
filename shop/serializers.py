from rest_framework import serializers
from .models import Category, Product, ProductImage, Attribute, CartItem, Cart, OrderItem, Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "image",
            "is_active",
            "created_at",
        )

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ("id", "type", "value")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    attributes = AttributeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "price",
            "is_featured",
            "stock",
            "created_at",
            "category",
            "attributes",
            "images",
        )



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            "items",
            "total_price",
            "total_items",
            "updated_at",
        )

    def get_total_price(self, obj):
        return obj.get_total_price()

    def get_total_items(self, obj):
        return obj.get_total_items_count()


class AddToCartSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)



class CreateOrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    shipping_address = serializers.CharField()
    phone_number = serializers.CharField()



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "user",
            "status",
            "total_amount",
            "shipping_address",
            "phone_number",
            "created_at",
            "updated_at",
            "items",
            "total_items",
        )

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.order_items.all())