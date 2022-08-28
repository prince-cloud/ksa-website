from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [ 'username','get_full_name', 'phone_number', 'email',]
    fieldsets = [
        *UserAdmin.fieldsets,
    ]
    fieldsets.insert(
        2,
        (
            "Profile Information",
            {
                "fields": (                  
                    "phone_number",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)