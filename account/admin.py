from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import TempUserBeforeActive

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'staff', 'admin', 'status')
    list_filter = ('staff', 'admin', 'status', 'create_date', 'update_date')

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'profile_picture', 'description')
        }),
        ('Contact info', {
            'fields': ('phone', 'address', 'city', 'state', 'zip_postal_code', 'country')
        }),
        ('Other info', {
            'fields': ('title', 'pic_full_name', 'position', 'website')
        }),
        ('Permissions', {
            'fields': ('role', 'staff', 'admin', 'status')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

admin.site.unregister(Group)

class TempUserBeforeActiveAdmin(admin.ModelAdmin):
    list_display = ('slug', 'email', 'create_date', 'update_date')
    list_filter = ('create_date', 'update_date')
    search_fields = ('hash_object',)

admin.site.register(TempUserBeforeActive, TempUserBeforeActiveAdmin)
