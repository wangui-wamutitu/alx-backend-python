from django.contrib import admin
from .models import Message, Conversation, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ("user_id", "email", "username", "first_name", "last_name", "role", "is_staff")
    search_fields = ("email", "username")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "password1", "password2", "role", "is_active", "is_staff"),
        }),
    )


admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(User, CustomUserAdmin)

