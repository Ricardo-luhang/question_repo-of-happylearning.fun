from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['real_name', 'mobile', 'qq', 'avator', 'avator_sm']
    search_fields = ['real_name', 'mobile', 'qq', 'avator', 'avator_sm']
    list_filter = ['real_name', 'mobile', 'qq', 'avator', 'avator_sm']


admin.site.register(User, UserAdmin)
