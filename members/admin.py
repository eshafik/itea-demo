from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from members.models import User, Profile


class UserAdmin(BaseUserAdmin):
    ordering = ['-id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {
            "fields": (
                'email',
                'password'
            ),
        }),
        (_('Personal Info'), {
            "fields": (
                'name',
                'designation'
            ),
        }),
        (_('Permissions'), {
            "fields": (
                'is_active',
                'is_internal',
                'is_staff',
                'is_superuser',
                'user_permissions',
                'groups',
            ),
        }),
        (_('Important dates'), {
            "fields": (
                'last_login',
            ),
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": (
                'wide',
            ),
            "fields": (
                'name',
                'email',
                'password1',
                'password2',
                'is_internal',
            )
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
