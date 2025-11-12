from django.contrib import admin
from django.db.models import Sum

from .models import Category, Attribute, Product, ProductImage, CartItem, Cart, OrderItem, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("type", "value")
    search_fields = ("value",)
    list_filter = ("type",)



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_featured", "stock", "created_at")
    search_fields = ("name",)
    list_filter = ("category", "is_featured", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]



class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "total_items", "total_price", "updated_at")
    search_fields = ("user__username", "user__email")
    inlines = [CartItemInline]

    # helper columns calling model methods
    def total_price(self, obj):
        return obj.get_total_price()

    def total_items(self, obj):
        return obj.get_total_items_count()



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)
    readonly_fields = ()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "items_count", "total_amount", "created_at")
    search_fields = ("order_number", "user__username", "user__email", "phone_number")
    list_filter = ("status", "created_at")
    readonly_fields = ("created_at", "updated_at")
    inlines = [OrderItemInline]

    def items_count(self, obj):
        return obj.order_items.aggregate(total=Sum("quantity")).get("total") or 0