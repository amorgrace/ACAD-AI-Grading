
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'student_id',         
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'date_joined'
    )
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'student_id') 
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Student Info', {'fields': ('student_id', 'courses')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'courses',
                'is_staff',
                'is_active',
            ),
        }),
    )
    
    readonly_fields = (
        'student_id',   
        'last_login',
        'date_joined'
    )
    