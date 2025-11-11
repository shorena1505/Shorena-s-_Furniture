from django.contrib import admin
from .models import Category, Attribute, Product, ProductImage


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
