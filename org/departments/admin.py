from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class AuthorAdmin(admin.ModelAdmin):
    pass
