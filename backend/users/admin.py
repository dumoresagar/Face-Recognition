from django.contrib import admin
from users.models import (User,Role,)
from .forms import UserCreationForm
from import_export.admin import ImportExportModelAdmin
from django import forms

class UserAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    form = UserCreationForm
    list_display = [
        'id', 'username', 'email',
        'date_created', 'date_updated', 'active_status','is_deleted',  
    ]
    list_display_links=['id','username']
    exclude = ['peram_group']




class RoleAdminForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = "__all__"


class RoleAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    form =RoleAdminForm 
    list_display = [
        "role_name",
    ]




admin.site.register(User,UserAdmin)
admin.site.register(Role,RoleAdmin)
