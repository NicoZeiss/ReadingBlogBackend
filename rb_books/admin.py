from django.contrib import admin

from .models import Volume, Author, Editor, Audience, Category, Rating, Book


class VolumeAdmin(admin.ModelAdmin):
    list_display = ('label', 'code',)


class AuthorAdmin(admin.ModelAdmin):
    pass


class EditorAdmin(admin.ModelAdmin):
    pass


class AudienceAdmin(admin.ModelAdmin):
    list_display = ('label', 'short_label',)


class CategoryAdmin(admin.ModelAdmin):
    pass


class RatingAdmin(admin.ModelAdmin):
    list_display = ('label', 'rating',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'editor', 'audience', 'rating', 'published', 'created_at',)


admin.site.register(Volume, VolumeAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Audience, AudienceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Book, BookAdmin)
