from django.db import models
from django.utils.html import mark_safe
from django.templatetags.static import static

from django_ckeditor_5.fields import CKEditor5Field

from slugify import slugify


class SlugifiedModel(models.Model):
    """
    Abstract model which integrate a slug field
    """
    FIELDS_TO_SLUGIFY = []

    slug = models.SlugField(
        max_length=150,
        unique=True
    )

    class Meta:
        abstract = True

    def _convert_fields_name_to_value(self) -> list[str]:
        return [str(getattr(self, field)) for field in self.FIELDS_TO_SLUGIFY]

    def _get_string_to_slugify(self) -> str:
        if len(self.FIELDS_TO_SLUGIFY) == 0:
            return self.__str__()
        return " ".join(self._convert_fields_name_to_value())

    def save(self, *args, **kwargs):
        self.slug = slugify(self._get_string_to_slugify())
        return super().save(*args, **kwargs)


class Volume(SlugifiedModel):
    """
    Model to represent a Volume object
    """
    label = models.CharField(
        verbose_name='Label',
        max_length=15,
        unique=True
    )
    code = models.CharField(
        verbose_name='Code',
        max_length=5
    )

    class Meta:
        verbose_name = 'Volume'

    def __str__(self):
        return self.label.capitalize()


class Author(SlugifiedModel):
    """
    Model to represent an Author object
    """
    first_name = models.CharField(
        verbose_name='Prénom',
        max_length=50
    )
    last_name = models.CharField(
        verbose_name='Nom de famille',
        max_length=50
    )

    class Meta:
        verbose_name = 'Auteur'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.first_name.capitalize()} {self.last_name.upper()}'


class Editor(SlugifiedModel):
    """
    Model to represent an Editor object
    """
    name = models.CharField(
        verbose_name='Nom',
        max_length=150,
        unique=True
    )

    class Meta:
        verbose_name = 'Éditeur'

    def __str__(self):
        return self.name.capitalize()


class Audience(SlugifiedModel):
    """
    Model to represent an Audience object
    """
    label = models.CharField(
        verbose_name='Label',
        max_length=50,
        unique=True
    )
    short_label = models.CharField(
        verbose_name='Label court',
        max_length=50,
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Public'

    def __str__(self):
        return self.label.capitalize()


class Genre(SlugifiedModel):
    """
    Model to represent a Genre object
    """
    label = models.CharField(
        verbose_name='Label',
        max_length=50,
        unique=True
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True
    )
    example_book = models.ForeignKey(
        to='Book',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Livre exemple'
    )

    class Meta:
        verbose_name = 'Genre'

    def __str__(self):
        return self.label.capitalize()


class Rating(SlugifiedModel):
    """
    Model to represent a Rating object
    """
    label = models.CharField(
        verbose_name='Label',
        max_length=150
    )
    code = models.CharField(
        verbose_name='Code',
        max_length=5,
        unique=True
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True
    )
    rating = models.PositiveIntegerField(
        verbose_name='Note',
        unique=True
    )

    class Meta:
        verbose_name = 'Note'

    def __str__(self):
        return self.label.capitalize()


class Category(SlugifiedModel):
    """
    Model to represent a Category object
    """
    label = models.CharField(
        verbose_name='Label',
        max_length=50,
        unique=True
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Catégorie'

    def __str__(self):
        return self.label.capitalize()


class BookBase(SlugifiedModel):
    """
    Abstract base class for Book and Collection
    """
    title = models.CharField(
        verbose_name='Titre',
        max_length=150
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Auteur'
    )
    editor = models.ForeignKey(
        Editor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Éditeur'
    )
    audience = models.ForeignKey(
        Audience,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Public'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Catégorie'
    )
    genres = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Genres'
    )
    summary = models.TextField(
        verbose_name='Résumé',
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name='Couverture',
        upload_to='covers/',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def img_preview(self):
        image_url = self.image.url if self.image else static('/img/empty-book.jpg')
        return mark_safe(f'<img src = "{image_url}" width = "100" />')


class Collection(BookBase):
    """
    Model to represent a Collection object
    """
    volumes_count = models.PositiveIntegerField(
        verbose_name='Nombre de volumes',
        null=True,
        blank=True
    )
    complete = models.BooleanField(
        verbose_name='Collection complète',
        default=False
    )

    class Meta:
        verbose_name = 'Collection'

    def __str__(self):
        return self.title


class Book(BookBase):
    """
    Model to represent a Book object
    """
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Collection'
    )
    sub_title = models.CharField(
        verbose_name='Sous-titre',
        max_length=150,
        null=True,
        blank=True
    )
    volume = models.ForeignKey(
        Volume,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Volume'
    )
    price = models.DecimalField(
        verbose_name='Prix',
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    pages = models.PositiveIntegerField(
        verbose_name='Pages',
        null=True,
        blank=True
    )
    quotation = models.TextField(
        verbose_name='Citation',
        null=True,
        blank=True
    )
    opinion = CKEditor5Field(
        verbose_name='Avis détaillé',
        null=True,
        blank=True
    )
    short_opinion = models.TextField(
        verbose_name='Avis résumé',
        null=True,
        blank=True
    )
    rating = models.ForeignKey(
        Rating,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Note'
    )
    about = CKEditor5Field(
        verbose_name='Au sujet du livre',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Date création',
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name='Date modification',
        auto_now=True
    )
    published = models.BooleanField(
        verbose_name='Publié',
        default=False
    )
    published_at = models.DateTimeField(
        verbose_name='Date publication',
        null=True,
        blank=True
    )
    current_reading = models.BooleanField(
        verbose_name='En cours de lecture',
        default=False
    )
    incoming_reading = models.BooleanField(
        verbose_name='Lecture à venir',
        default=False
    )

    class Meta:
        verbose_name = 'Livre'

    def __str__(self):
        return self.full_title

    def save(self, *args, **kwargs):
        if self.belongs_to_collection:
            self._match_collection_attributes()
        return super().save(*args, **kwargs)

    @property
    def full_title(self):
        parts = [part for part in [self.title, self.volume.label if self.volume else None, self.sub_title] if part]
        return ' - '.join(parts)

    @property
    def belongs_to_collection(self):
        """
        Return if instance belongs to a Collection
        :return: Boolean
        """
        return self.collection is not None

    def _match_collection_attributes(self):
        """
        Method to match collection attributes with instance attributes
        """
        if self.sub_title is None or self.sub_title == '':
            self.sub_title = self.title
        self.title = self.collection.title

        self.author = self.collection.author
        self.editor = self.collection.editor
        self.audience = self.collection.audience
        self.category = self.collection.category
