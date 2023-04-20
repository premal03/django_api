from django.contrib import admin

# Register your models here.
from .models import Students, Singer, Song


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rollno','city']


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'singer', 'duration']
