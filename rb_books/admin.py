from django.contrib import admin

from .models import Author, Editor, Audience, Genre, Rating, Series, Book, Category, Illustrator


class CustomModelAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions_on_top = False

    exclude = ['slug']


class AuthorAdmin(CustomModelAdmin):
    search_fields = ['first_name', 'last_name']


class IllustratorAdmin(CustomModelAdmin):
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


class SeriesAdmin(CustomModelAdmin):
    list_display = [
        'img_preview', 'title', 'show_title', 'illustrator', 'editor', 'audience', 'volumes_count',
        'complete',
    ]
    list_display_links = [
        'img_preview', 'title',
    ]
    list_editable = [
        'complete', 'show_title',
    ]

    fieldsets = [
        (
            None,
            {
                'fields': ['title', 'show_title', 'author', 'illustrator', 'editor', 'image', 'img_preview']
            },
        ),
        (
            'Informations détaillées',
            {
                'fields': ['audience', 'category', 'genres', 'summary', 'volumes_count', 'complete',]
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
        'title', 'author__first_name', 'author__last_name', 'illustrator__first_name', 'illustrator__last_name',
        'editor__name',
    ]


class BookAdmin(CustomModelAdmin):
    """
    The `BookAdmin` class is a custom model admin class that is used to customize the administration interface for the
     `Book` model in the application.
    Attributes:
        - `list_display`: A list of fields to be displayed in the list view of the administration interface.
        - `list_display_links`: A list of fields that should be linked to the change view of the administration
        interface.
        - `list_editable`: A tuple of fields that can be edited directly in the list view of the administration
        interface.
        - `fieldsets`: A list of fieldsets to be displayed in the create/update forms of the administration interface.
        - `readonly_fields`: A list of fields that are readonly in the administration interface.
        - `search_fields`: A list of fields that can be searched in the administration interface.
        - `list_filter`: A list of fields that can be used for filtering in the administration interface.
    Note: This class extends the `CustomModelAdmin` class.
    """
    # List parameters
    list_display = [
        'img_preview', '__str__', 'series', 'illustrator', 'editor', 'audience', 'rating', 'incoming_reading',
        'current_reading', 'published', 'published_at', 'created_at',
    ]
    list_display_links = [
        'img_preview', '__str__',
    ]
    list_editable = (
        'incoming_reading', 'current_reading', 'published',
    )

    # Create/Update forms
    fieldsets = [
        (
            None,
            {
                'fields': ['title', 'volume', 'series', 'author', 'illustrator', 'editor', 'image', 'img_preview']
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
                'fields': [
                    'about', 'incoming_reading', 'current_reading', 'published', 'published_at', 'created_at', 'slug'
                ]
            }
        ),
    ]
    readonly_fields = [
        'slug', 'created_at', 'img_preview',
    ]

    # Search/Filter
    search_fields = [
        'title', 'volume__label', 'author__first_name', 'author__last_name', 'illustrator__first_name',
        'illustrator__last_name', 'editor__name',
    ]
    list_filter = [
        'audience', 'rating', 'incoming_reading', 'current_reading', 'published', 'published_at',
    ]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Illustrator, IllustratorAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Audience, AudienceAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Book, BookAdmin)

# TODO: se renseigner sur l'app facultative FlatPages de Django

# TODO: customiser panel admin natif
