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


class Category(models.Model):
    """
    Model to represent a Category object
    """
    label = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

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


class Book(models.Model):
    """
    Model to represent a Book object
    """
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=150, null=True, blank=True)
    volume = models.ForeignKey(Volume, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.PositiveIntegerField(null=True, blank=True)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    editor = models.ForeignKey(Editor, null=True, on_delete=models.SET_NULL)
    audience = models.ForeignKey(Audience, null=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(Category)
    summary = models.TextField(null=True, blank=True)
    quotation = models.TextField(null=True, blank=True)
    opinion = models.TextField(null=True, blank=True)
    short_opinion = models.TextField(null=True, blank=True)
    rating = models.ForeignKey(Rating, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        if self.sub_title is None or self.sub_title == '':
            return self.title
        return f'{self.title} - {self.volume.label} - {self.sub_title}'
