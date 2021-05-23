from django.contrib import admin
from .models import Ad, Category

admin.site.register(Category)
admin.site.register(Ad)