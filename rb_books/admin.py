from django.contrib import admin

from .models import Volume, Author, Editor, Audience, Category, Rating, Book


class VolumeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Volume, VolumeAdmin)
