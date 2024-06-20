
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from django.contrib.auth.models import Group

from .EcwForms import CustomUserCreationForm, CustomUserChangeForm
from .models import EcwUser,EcwGroup

#admin.site.unregister(Group)

@admin.register(EcwGroup)
class CustomGroupAdmin(GroupAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'permissions')}),
        (('Description'), {'fields': ('description',)}),
    )


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = EcwUser
    list_display = ("email", "is_staff", "is_active","branch","group","firstname","lastname","needs_password_change",)
    list_filter = ("email", "is_staff", "is_active","branch","group","firstname","lastname","needs_password_change",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "firstname","lastname","branch","group","needs_password_change","email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(EcwUser, CustomUserAdmin)