from django.db import models
from django.utils.html import mark_safe
from django.templatetags.static import static

from slugify import slugify


class Volume(models.Model):
    """
    Model to represent a Volume object
    """
    label = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=5)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        return super().save(*args, **kwargs)


class Author(models.Model):
    """
    Model to represent an Author object
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.first_name.capitalize()} {self.last_name.upper()}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        return super().save(*args, **kwargs)


class Editor(models.Model):
    """
    Model to represent an Editor object
    """
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Audience(models.Model):
    """
    Model to represent an Audience object
    """
    label = models.CharField(max_length=50, unique=True)
    short_label = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        return super().save(*args, **kwargs)


class Genre(models.Model):
    """
    Model to represent a Genre object
    """
    label = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    example_book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        return super().save(*args, **kwargs)


class Rating(models.Model):
    """
    Model to represent a Rating object
    """
    label = models.CharField(max_length=150)
    code = models.CharField(max_length=5, unique=True)
    description = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        return super().save(*args, **kwargs)


class Category(models.Model):
    """
    Model to represent a Category object
    """
    label = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        return super().save(*args, **kwargs)


class BookBase(models.Model):
    """
    Abstract base class for Book and Collection
    """
    title = models.CharField(max_length=150)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, blank=True)
    editor = models.ForeignKey('Editor', on_delete=models.SET_NULL, null=True, blank=True)
    audience = models.ForeignKey(Audience, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    summary = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='covers/', null=True, blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        abstract = True

    def img_preview(self):
        image_url = self.image.url if self.image else static('/img/empty-book.jpg')
        return mark_safe(f'<img src = "{image_url}" width = "100" />')


class Collection(BookBase):
    """
    Model to represent a Collection object
    """
    volumes_count = models.PositiveIntegerField(null=True, blank=True)
    complete = models.BooleanField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Book(BookBase):
    """
    Model to represent a Book object
    """
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True)
    sub_title = models.CharField(max_length=150, null=True, blank=True)
    volume = models.ForeignKey(Volume, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    quotation = models.TextField(null=True, blank=True)
    opinion = models.TextField(null=True, blank=True)
    short_opinion = models.TextField(null=True, blank=True)
    rating = models.ForeignKey(Rating, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    current_reading = models.BooleanField(default=False)
    incoming_reading = models.BooleanField(default=False)

    def __str__(self):
        return self.full_title

    def save(self, *args, **kwargs):
        if self.belongs_to_collection:
            self._match_collection_attributes()
        self.slug = slugify(self.full_title)
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
