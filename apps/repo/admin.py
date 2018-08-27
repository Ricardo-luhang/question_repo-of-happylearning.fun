from django.contrib import admin
from apps.repo.models import Category, Tag, Questions
# Register your models here.


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Questions)
