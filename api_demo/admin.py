from django.contrib import admin

# Register your models here.
from .models import Students

@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rollno','city']

