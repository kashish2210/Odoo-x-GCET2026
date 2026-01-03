from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ("login_id", "email", "role", "is_active")
    list_filter = ("role", "is_active")

    fieldsets = (
        (None, {"fields": ("login_id", "email", "password")}),
        ("Role & Permissions", {"fields": ("role", "is_staff", "is_superuser")}),
        ("Status", {"fields": ("is_active",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("login_id", "email", "password1", "password2"),
        }),
    )

    search_fields = ("login_id", "email")
    ordering = ("login_id",)
