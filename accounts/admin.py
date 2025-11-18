from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "phone", "address", "id", "is_staff")
    search_fields = ("username", "phone")
    list_filter = ("address", "is_staff", "is_superuser", "is_active", "groups")

    # show our custom fields on the user edit page
    fieldsets = UserAdmin.fieldsets + (
        ("Extra info", {"fields": ("phone", "address", "birth_date")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra info", {"fields": ("phone", "address", "birth_date")}),
    )
