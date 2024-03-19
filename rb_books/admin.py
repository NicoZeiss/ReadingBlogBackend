from django.contrib import admin

from .models import Volume, Author, Editor, Audience, Genre, Rating, Collection, Book


class VolumeAdmin(admin.ModelAdmin):
    list_display = (
        'label', 'code',
    )


class AuthorAdmin(admin.ModelAdmin):
    pass


class EditorAdmin(admin.ModelAdmin):
    pass


class AudienceAdmin(admin.ModelAdmin):
    list_display = (
        'label', 'short_label',
    )


class GenreAdmin(admin.ModelAdmin):
    pass


class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'label', 'rating',
    )


class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        'img_preview', 'title', 'author', 'editor', 'audience', 'volumes_count', 'complete',
    )
    list_display_links = (
        'img_preview', 'title',
    )
    readonly_fields = (
        'img_preview',
    )
    list_editable = (
        'complete',
    )
    list_filter = (
        'audience', 'complete',
    )
    search_fields = (
        'title', 'author__first_name', 'author__last_name', 'editor__name',
    )


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'img_preview', '__str__', 'author', 'editor', 'audience', 'rating', 'incoming_reading', 'current_reading',
        'published', 'published_at', 'created_at',
    )
    list_display_links = (
        'img_preview', '__str__',
    )
    readonly_fields = (
        'published_at', 'img_preview',
    )
    list_editable = (
        'rating', 'incoming_reading', 'current_reading', 'published',
    )
    search_fields = (
        'title', 'sub_title', 'volume__label', 'author__first_name', 'author__last_name', 'editor__name',
    )
    list_filter = (
        'audience', 'rating', 'incoming_reading', 'current_reading', 'published', 'published_at',
    )


admin.site.register(Volume, VolumeAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Audience, AudienceAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Book, BookAdmin)
