from django.db import models


class Volume(models.Model):
    """
    Model to represent a Volume object
    """
    label = models.CharField(max_length=15)
    code = models.CharField(max_length=5)

    def __str__(self):
        return self.label


class Author(models.Model):
    """
    Model to represent an Author object
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name.capitalize()} {self.last_name.upper()}'


class Editor(models.Model):
    """
    Model to represent an Editor object
    """
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Audience(models.Model):
    """
    Model to represent an Audience object
    """
    label = models.CharField(max_length=50)
    short_label = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.label


class Genre(models.Model):
    """
    Model to represent a Genre object
    """
    label = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    example_book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.label


class Rating(models.Model):
    """
    Model to represent a Rating object
    """
    label = models.CharField(max_length=150)
    code = models.CharField(max_length=5)
    description = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return self.label


class CategoryBase(models.Model):
    """
    Model to represent a Category object
    """
    label = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)


class BookBase(models.Model):
    """
    Abstract base class for Book and Collection
    """
    title = models.CharField(max_length=150)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, blank=True)
    editor = models.ForeignKey('Editor', on_delete=models.SET_NULL, null=True)
    audience = models.ForeignKey(Audience, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(CategoryBase, on_delete=models.SET_NULL, null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    summary = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class Collection(BookBase):
    """
    Model to represent a Collection object
    """
    volumes_count = models.PositiveIntegerField(null=True, blank=True)
    complete = models.BooleanField()

    def __str__(self):
        return self.title


class Book(BookBase):
    """
    Model to represent a Book object
    """
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True)
    sub_title = models.CharField(max_length=150, null=True, blank=True)
    volume = models.ForeignKey(Volume, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.PositiveIntegerField(null=True, blank=True)
    quotation = models.TextField(null=True, blank=True)
    opinion = models.TextField(null=True, blank=True)
    short_opinion = models.TextField(null=True, blank=True)
    rating = models.ForeignKey(Rating, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        if self.sub_title is None or self.sub_title == '':
            return self.title
        return f'{self.title} - {self.volume.label} - {self.sub_title}'

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
        pass
        if self.sub_title is None or self.sub_title == '':
            self.sub_title = self.title
        self.title = self.collection.title

        self.author = self.collection.author
        self.editor = self.collection.editor
        self.audience = self.collection.audience
        self.category = self.collection.category

    def save(self, *args, **kwargs):
        """
        Override save method to match instance attributes with collection attributes when needed
        """
        if self.belongs_to_collection:
            self._match_collection_attributes()
        return super().save(*args, **kwargs)
