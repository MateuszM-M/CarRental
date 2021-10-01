from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'city',
                    'street', 'number', 'phone')
    
admin.site.register(Profile, ProfileAdmin)
