from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _
from .models import User, nonLoginUser, Table


# Register your models here.
class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name',)


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'name', 'logo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'logo'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('name', 'formatted_logo', 'last_login')
    search_fields = ('name',)
    ordering = ('name',)


class nonLoginUserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'allowed', 'table', 'price', 'active', 'nomiho',
                    'nomiho_name', 'nomiho_price', 'created_at')
    list_editable = ('allowed', 'table', 'price', 'active', 'nomiho',
                     'nomiho_name', 'nomiho_price')
    ordering = ('-created_at',)


class TableAdmin(admin.ModelAdmin):
    list_display = ('table', 'price', 'active', 'user', 'created_at')
    list_editable = ('price', 'active', 'user')
    ordering = ('-created_at',)


admin.site.register(User, MyUserAdmin)
admin.site.register(nonLoginUser, nonLoginUserAdmin)
admin.site.register(Table, TableAdmin)
