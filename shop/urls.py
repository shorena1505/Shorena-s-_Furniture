from django.urls import path
from shop.views import CategoryListView, ProductListView, ProductDetailView, CartView, OrderDetailView, OrderListView, \
    AddToCartView, CreateOrderView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("cart/<int:user_id>/", CartView.as_view(), name="cart-detail"),
    path("cart/add/", AddToCartView.as_view(), name="cart-add"),
    path("orders/<int:user_id>/", OrderListView.as_view(), name="order-list"),
    path("orders/detail/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/create/", CreateOrderView.as_view(), name="order-create"),

]
