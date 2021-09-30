from django.contrib import admin
from .models import Profile
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'city',
                    'street', 'number', 'phone')
admin.site.register(Profile, ProfileAdmin)
