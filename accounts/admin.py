from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, AIAgentConfig


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription_expiry', 'package_name']
    actions = ['assign_7_days', 'assign_15_days', 'assign_30_days']
    
    def assign_days(self, request, queryset, days, package_name):
        from django.utils import timezone
        from datetime import timedelta
        
        expiry_date = timezone.now() + timedelta(days=days)
        updated_count = queryset.update(
            subscription_expiry=expiry_date,
            package_name=package_name
        )
        self.message_user(request, f"{updated_count} users assigned {package_name} package.")
    
    @admin.action(description="Assign 7 Days Package")
    def assign_7_days(self, request, queryset):
        self.assign_days(request, queryset, 7, "7 Days Pack")
    
    @admin.action(description="Assign 15 Days Package")
    def assign_15_days(self, request, queryset):
        self.assign_days(request, queryset, 15, "15 Days Pack")
    
    @admin.action(description="Assign 30 Days Package")
    def assign_30_days(self, request, queryset):
        self.assign_days(request, queryset, 30, "30 Days Pack")


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(UserProfile) # Replaced with custom admin class
admin.site.register(AIAgentConfig)
