from apps.bonds.models import Bond
from apps.users.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class BondInline(admin.TabularInline):
    model = Bond
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [BondInline]
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
