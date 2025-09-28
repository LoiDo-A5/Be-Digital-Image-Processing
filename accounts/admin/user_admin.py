from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'avatar',
                    'birthday', 'is_phone_verified')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email', 'phone_number', 'birthday')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'birthday')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('avatar', 'is_phone_verified')}),
    )
