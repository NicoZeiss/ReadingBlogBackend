from django.contrib import admin

from .models import Volume, Author, Editor, Audience, Genre, Rating, Collection, Book


class VolumeAdmin(admin.ModelAdmin):
    list_display = ('label', 'code',)


class AuthorAdmin(admin.ModelAdmin):
    pass


class EditorAdmin(admin.ModelAdmin):
    pass


class AudienceAdmin(admin.ModelAdmin):
    list_display = ('label', 'short_label',)


class GenreAdmin(admin.ModelAdmin):
    pass


class RatingAdmin(admin.ModelAdmin):
    list_display = ('label', 'rating',)


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'editor', 'audience', 'complete',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'editor', 'audience', 'rating', 'published', 'created_at',)


admin.site.register(Volume, VolumeAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Audience, AudienceAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Book, BookAdmin)
