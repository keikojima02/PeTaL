from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import PetalUserCreationForm, PetalUserChangeForm

PetalUser = get_user_model()

class PetalUserAdmin(UserAdmin):
    add_form = PetalUserCreationForm

    form = PetalUserChangeForm
    model = PetalUser
    list_display = ['email', 'username',]


admin.site.register(PetalUser, PetalUserAdmin)