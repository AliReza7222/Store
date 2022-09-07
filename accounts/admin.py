from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class AdminUser(admin.ModelAdmin):
    fields = [
        ('username', 'password'),
        ('first_name', 'last_name'),
        'email',
        ('is_active', 'is_staff', 'is_superuser'),
        'groups',
        'user_permissions'
    ]
    filter_horizontal = ['groups', 'user_permissions']
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_editable = ['is_staff', 'is_active']
