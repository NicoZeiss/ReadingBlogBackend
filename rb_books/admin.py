from django.contrib import admin

from .models import Volume, Author, Editor, Audience, Genre, Rating, Collection, Book


class CustomModelAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions_on_top = False

    exclude = ['slug']


class VolumeAdmin(CustomModelAdmin):
    list_display = [
        'label', 'code',
    ]


class AuthorAdmin(CustomModelAdmin):
    pass


class EditorAdmin(CustomModelAdmin):
    pass


class AudienceAdmin(CustomModelAdmin):
    list_display = [
        'label', 'short_label',
    ]


class GenreAdmin(CustomModelAdmin):
    pass


class RatingAdmin(CustomModelAdmin):
    list_display = [
        'label', 'rating',
    ]


class CollectionAdmin(CustomModelAdmin):
    list_display = [
        'img_preview', 'title', 'author', 'editor', 'audience', 'volumes_count', 'complete',
    ]
    list_display_links = [
        'img_preview', 'title',
    ]
    readonly_fields = [
        'img_preview',
    ]
    list_editable = [
        'complete',
    ]
    list_filter = [
        'audience', 'complete',
    ]
    search_fields = [
        'title', 'author__first_name', 'author__last_name', 'editor__name',
    ]


class BookAdmin(CustomModelAdmin):
    # List parameters
    list_display = [
        'img_preview', '__str__', 'author', 'editor', 'audience', 'rating', 'incoming_reading', 'current_reading',
        'published', 'published_at', 'created_at',
    ]
    list_display_links = [
        'img_preview', '__str__',
    ]
    list_editable = (
        'rating', 'incoming_reading', 'current_reading', 'published',
    )

    # Create/Update forms
    fields = [
        'title', 'volume', 'collection', 'sub_title', 'author', 'editor', 'pages', 'price', 'category', 'genres',
        'summary', 'opinion', 'short_opinion', 'quotation', 'rating', 'incoming_reading', 'current_reading',
        'published', 'published_at', 'created_at', 'img_preview',
    ]
    readonly_fields = [
        'published_at', 'created_at', 'img_preview',
    ]

    # Search/Filter
    search_fields = [
        'title', 'sub_title', 'volume__label', 'author__first_name', 'author__last_name', 'editor__name',
    ]
    list_filter = [
        'audience', 'rating', 'incoming_reading', 'current_reading', 'published', 'published_at',
    ]


admin.site.register(Volume, VolumeAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Audience, AudienceAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Book, BookAdmin)

# TODO: Dans Book supprimer le subtitle, et considérer que le title est le titre d'un volume. Si title vide, alors on
#  copie title de collection
# TODO: se renseigner sur l'app facultative FlatPages de Django
# TODO: regarder fonctionnement des Validators (voir si ça peut servir pour valider titre/collection)
