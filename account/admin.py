from typing import Any, Dict, List, Optional, Tuple
from django.contrib import admin
from django.http.request import HttpRequest
from django.contrib.auth.models import Group

# Register your models here.
from .models import CustomUser

class GroupAdminInline(admin.ModelAdmin):
      pass


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display =('first_name','last_name','email','is_admin','is_active','password')
    
    readonly_fields = ('first_name','last_name','email','password')
    
    exclude = ['last_login']
    
    fieldsets = (
        ('Personal Information', {'fields': ('first_name','last_name','email','is_admin','is_active','password')}),
        ('Permissions', {'fields':('is_superuser', 'groups', 'user_permissions')}),
        ('Custom Field Permissions', {'fields':('custom_field',)}),
    )
    
    def get_fieldsets(self, request, obj=None):
        if request.user.has_perm('your_app_name.can_edit_custum_field'):
          return self.fieldsets
        return super().get_fieldsets(request, obj)
        


admin.site.register(CustomUser, CustomUserAdmin)
