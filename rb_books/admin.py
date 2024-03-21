from django.contrib import admin

from .models import Volume, Author, Editor, Audience, Genre, Rating, Collection, Book, Category


class CustomModelAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions_on_top = False

    exclude = ['slug']


class VolumeAdmin(CustomModelAdmin):
    list_display = [
        'label', 'code',
    ]


class AuthorAdmin(CustomModelAdmin):
    search_fields = ['first_name', 'last_name']


class EditorAdmin(CustomModelAdmin):
    search_fields = ['name']


class AudienceAdmin(CustomModelAdmin):
    list_display = ['label', 'short_label']
    list_display_links = ['label', 'short_label']


class GenreAdmin(CustomModelAdmin):
    list_display = ['label', 'example_book']


class CategoryAdmin(CustomModelAdmin):
    list_display = ['label']


class RatingAdmin(CustomModelAdmin):
    list_display = ['label', 'rating']
    list_display_links = ['label', 'rating']


class CollectionAdmin(CustomModelAdmin):
    list_display = [
        'img_preview', 'title', 'author', 'editor', 'audience', 'volumes_count', 'complete',
    ]
    list_display_links = [
        'img_preview', 'title',
    ]
    list_editable = [
        'complete',
    ]

    fieldsets = [
        (
            None,
            {
                'fields': ['title', 'author', 'editor', 'image', 'img_preview']
            },
        ),
        (
            'Informations détaillées',
            {
                'fields': ['audience', 'category', 'genres', 'summary', 'volumes_count', 'complete']
            }
        )
    ]
    readonly_fields = [
        'img_preview',
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
    fieldsets = [
        (
            None,
            {
                'fields': ['title', 'volume', 'collection', 'sub_title', 'author', 'editor', 'image', 'img_preview']
            },
        ),
        (
            'Informations détaillées',
            {
                'fields': ['audience', 'pages', 'price', 'category', 'genres', 'summary']
            }
        ),
        (
            'Avis',
            {
                'fields': ['opinion', 'short_opinion', 'quotation', 'rating']
            }
        ),
        (
            'Publication',
            {
                'fields': ['about', 'incoming_reading', 'current_reading', 'published', 'published_at', 'created_at']
            }
        ),
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
admin.site.register(Category, CategoryAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Book, BookAdmin)

# TODO: Dans Book supprimer le subtitle, et considérer que le title est le titre d'un volume. Si title vide, alors on
#  copie title de collection

# TODO: se renseigner sur l'app facultative FlatPages de Django

# TODO: regarder fonctionnement des Validators (voir si ça peut servir pour valider titre/collection)

# TODO: définir rep de stockage images de manière dynamique pour éviter dossiers trop volumineux,
#  par ex : datetime.now().strftime('markdownx/%Y/%m/%d').
#  Source https://neutronx.github.io/django-markdownx/customization/

# TODO: customiser panel admin natif

# TODO: generer logo.ico pour Jazzmin
