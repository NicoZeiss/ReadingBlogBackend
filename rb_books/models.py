from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe
from django.templatetags.static import static

from django_ckeditor_5.fields import CKEditor5Field

from slugify import slugify

from .utils import dynamic_upload_img_path


class SlugifiedModel(models.Model):
    """
    A base class that provides slugification functionality for models.
    Attributes:
        FIELDS_TO_SLUGIFY (list): A list of fields to slugify.
    Fields:
        slug (SlugField): The slug field to store the slugified value.
    Meta:
        abstract (bool): Specifies that this model is an abstract base class.
    Methods:
        _convert_fields_name_to_value(): Converts the values of fields specified in FIELDS_TO_SLUGIFY to strings and
        returns them as a list.
        _get_string_to_slugify(): Returns the string to slugify by joining the converted field values with space.
        save(*args, **kwargs): Overrides the save method of the parent class to slugify the string and save it to the
        slug field.
    """
    FIELDS_TO_SLUGIFY = []

    slug = models.SlugField(
        max_length=150,
        unique=True
    )

    class Meta:
        abstract = True

    def _convert_fields_name_to_value(self) -> list[str]:
        """
        Method Name: _convert_fields_name_to_value
        Description:
        This method converts the values of specified fields to strings and returns them as a list. It uses the
        FIELDS_TO_SLUGIFY attribute of the object to determine which fields to convert
        *.
        Parameters:
        - self: The object reference.
        Return Type:
        list[str]
        """
        return [str(getattr(self, field)) for field in self.FIELDS_TO_SLUGIFY]

    def _get_string_to_slugify(self) -> str:
        """
        Get the string to slugify.
        Returns:
            str: The string to slugify.
        Notes:
            This method checks if there are any fields specified to be slugified in the `FIELDS_TO_SLUGIFY` list
            attribute of the object. If not, it returns the string representation of the
        * object using the `__str__()` method. Otherwise, it concatenates the values of the fields specified in
        `FIELDS_TO_SLUGIFY` with a space character.
        """
        if len(self.FIELDS_TO_SLUGIFY) == 0:
            return self.__str__()
        return " ".join(self._convert_fields_name_to_value())

    def save(self, *args, **kwargs):
        """
        Save method.
        Sets the slug attribute of the object by slugifying the string obtained from `_get_string_to_slugify()` method
        and then calls the `save()` method of the superclass.
        Parameters:
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.
        Returns:
        - None.
        """
        self.slug = slugify(self._get_string_to_slugify())
        return super().save(*args, **kwargs)


class Volume(SlugifiedModel):
    """
    A class representing a Volume, which is a subclass of SlugifiedModel.
    Attributes:
        label (CharField): The label of the Volume, with a maximum length of 15 characters and must be unique.
        index (FloatField): The index of the Volume, must be unique.
    Meta:
        verbose_name (str): The human-readable name for the Volume class in the admin interface.
    Methods:
        __str__(): Returns the capitalized label of the Volume.
    Usage:
        volume = Volume(label='Volume 1', index=1.0)
        print(volume)  # Output: 'Volume 1'
    """
    label = models.CharField(
        verbose_name='Label',
        max_length=15,
        unique=True
    )
    index = models.FloatField(
        verbose_name='Index',
        unique=True,
    )

    class Meta:
        verbose_name = 'Tome'

    def __str__(self):
        return self.label.capitalize()


class Author(SlugifiedModel):
    """This class represents an author.
    Attributes:
        first_name (char): The first name of the author.
        last_name (char): The last name of the author.
    Meta:
        verbose_name (str): The verbose name of the author.
    Methods:
        __str__(): Returns a string representation of the author.
        full_name(): Returns the full name of the author.
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
        """
        This method, `full_name`, is a property method that returns the full name of an object. It takes no parameters.
        Returns:
            string: The full name of the object, in the format "{first_name} {last_name}".
        """
        return f'{self.first_name.capitalize()} {self.last_name.upper()}'


class Editor(SlugifiedModel):
    """
    The Editor class represents an editor for a publishing platform.
    Attributes:
        name (CharField): The name of the editor.
    Meta:
        verbose_name (str): The human-readable name of the editor model.
    Methods:
        __str__(): Returns a string representation of the editor's name.
    Inherited Attributes:
        - All attributes inherited from the SlugifiedModel base class.
    Inherited Methods:
        - All methods inherited from the SlugifiedModel base class.
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
    Audience Class
    A class representing an audience.
    Attributes:
        label (str): The label of the audience.
        short_label (str): The short label of the audience.
        description (str): The description of the audience.
    Methods:
        __str__(): Returns the capitalized label of the audience.
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
    Class representing a Genre.
    Inherits from SlugifiedModel.
    Attributes:
        label (CharField): The label of the genre.
        description (TextField): The description of the genre (optional).
        example_book (ForeignKey): A foreign key to a Book object that represents an example book for this genre
        (optional).
    Meta:
        verbose_name (str): The verbose name of the Genre model. Set to 'Genre'.
    Methods:
        __str__(): Returns the capitalized label of the genre.
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
    Definition of the Rating class.

    Inherits from SlugifiedModel.

    Attributes:
    - label: A character field representing the label of the rating.
    - description: A text field representing the description of the rating. It can be null and blank.
    - rating: A positive integer field representing the note of the rating. It must be unique.

    Meta:
    - verbose_name: A string representing the human-readable name of the class.

    Methods:
    - __str__(): Returns the capitalized label of the rating as a string.

    """
    label = models.CharField(
        verbose_name='Label',
        max_length=150
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
    A class representing a Category.

    Inherits from SlugifiedModel.

    Attributes:
        label (char): The label of the category.
        description (text): The description of the category.

    Meta:
        verbose_name (str): The verbose name of the category.

    Methods:
        __str__(): Returns the capitalized label of the category.

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
    The `BookBase` class is an abstract model class that serves as a base for creating book models in a Django project.
     It inherits from the `SlugifiedModel` model.
    Attributes:
    - `title`: A `CharField` that stores the title of the book.
    - `author`: A `ForeignKey` that references the `Author` model and represents the author of the book.
    - `editor`: A `ForeignKey` that references the `Editor` model and represents the editor of the book.
    - `audience`: A `ForeignKey` that references the `Audience` model and represents the target audience of the book.
    - `category`: A `ForeignKey` that references the `Category` model and represents the category of the book.
    - `genres`: A `ManyToManyField` that references the `Genre` model and represents the genres associated with the
    book.
    - `summary`: A `TextField` that stores the summary of the book.
    - `image`: An `ImageField` that stores the cover image of the book.
    Methods:
    - `img_preview()`: Returns an HTML string containing an `img` tag with the URL of the book's cover image. If the
    book doesn't have a cover image, a default image URL is used.
    Note: This is an abstract class and should not be instantiated directly.
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
    summary = CKEditor5Field(
        verbose_name='Résumé',
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name='Couverture',
        upload_to=dynamic_upload_img_path,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def img_preview(self):
        """
        Generates an HTML code for displaying an image preview.
        Parameters:
        self (object): The current instance of the class.
        Returns:
        str: HTML code for displaying the image preview.
        """
        image_url = self.image.url if self.image else static('/img/empty-book.jpg')
        return mark_safe(f'<img src = "{image_url}" width = "100" />')


class Series(BookBase):
    """
    A class representing a series of books.

    Attributes:
        volumes_count (PositiveIntegerField): The number of volumes in the series. Can be null or blank.
        complete (BooleanField): Indicates if the series is complete or not. Default is False.
        show_title (BooleanField): Indicates if the title should be shown or not. Default is True.

    Meta:
        verbose_name (str): The verbose name for the series.

    Methods:
        __str__(): Returns the string representation of the series.

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
    show_title = models.BooleanField(
        verbose_name='Afficher le titre',
        default=True
    )

    class Meta:
        verbose_name = 'Saga'

    def __str__(self):
        return self.title


class Book(BookBase):
    """
    Class representing a book.

    Attributes:
        title (char): The title of the book.
        series (ForeignKey): The series the book belongs to.
        volume (ForeignKey): The volume number of the book.
        price (decimal): The price of the book.
        pages (int): The number of pages in the book.
        quotation (text): A quotation from the book.
        opinion (CKEditor5Field): A detailed opinion about the book.
        short_opinion (text): A summary of the opinion about the book.
        rating (ForeignKey): The rating given to the book.
        about (CKEditor5Field): Information about the book.
        created_at (datetime): The date and time when the book was created.
        modified_at (datetime): The date and time when the book was last modified.
        published (bool): Whether the book has been published.
        published_at (datetime): The date and time when the book was published.
        current_reading (bool): Whether the book is currently being read.
        incoming_reading (bool): Whether the book is in the reading list.

    Methods:
        __str__(): Returns the full title of the book.
        clean(): Validates the book data before saving.
        save(*args, **kwargs): Saves the book to the database.
        _title_is_empty() -> bool: Checks if the title of the book is empty.
        _get_title_parts(): Returns a list of title parts for constructing the full title.
        full_title(): Returns the full title of the book.
        belongs_to_series(): Checks if the book belongs to a series.
        _match_collection_attributes(): Matches the collection attributes of the book with the series attributes.
    """
    title = models.CharField(
        verbose_name='Titre',
        max_length=150,
        null=True,
        blank=True
    )
    series = models.ForeignKey(
        Series,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Saga'
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
    quotation = CKEditor5Field(
        verbose_name='Citation',
        null=True,
        blank=True
    )
    opinion = CKEditor5Field(
        verbose_name='Avis détaillé',
        null=True,
        blank=True
    )
    short_opinion = CKEditor5Field(
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
        blank=True,
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
        """
        Return a string representation of the object.
        Parameters:
            self : object
                The instance of the object.
        Returns:
            str
                The string representation of the object.
        Example:
            obj = MyClass()
            print(obj.__str__())  # Prints the string representation of obj
        """
        return self.full_title

    def clean(self):
        """
        Clean the form data and perform additional validation.
        Raises:
            ValidationError: If a book has a volume but does not belong to a series, or if a book belongs to a series
            but does not have a volume.
        Returns:
            The cleaned form data after validation.
        """
        if self.volume is None and self.series is not None:
            raise ValidationError('Un livre ne peut pas appartenir à une saga sans avoir un numéro de tome.')
        elif self.volume is not None and self.series is None:
            raise ValidationError('Un livre ne peut pas être un tome sans appartenir à une saga.')
        return super().clean()

    def save(self, *args, **kwargs):
        """
        Save the object to the database.
        This method saves the object to the database. If the object belongs to a series, it calls the
        `_match_collection_attributes` method to match the collection attributes. Then, it cleans
        * the object using the `clean` method. Finally, it calls the `save` method of the superclass to save the object
         to the database.
        Parameters:
            *args: Optional arguments.
            **kwargs: Optional keyword arguments.
        Returns:
            None
        Example usage:
            save()
        """
        if self.belongs_to_series:
            self._match_collection_attributes()
        self.clean()
        return super().save(*args, **kwargs)

    @property
    def _title_is_empty(self) -> bool:
        """
        Check if the title is empty.
        :param self: The object instance.
        :return: True if the title is empty, False otherwise.
        :rtype: bool
        """
        return self.title is None or self.title == ''

    def _get_title_parts(self):
        """
        Returns the parts of the title for the current object.
        If the object belongs to a series and the series has a show_title flag set to True,
        the method returns a list containing the series title, the volume label, and the object's title.
        If the object does not belong to a series, the method returns a list containing only the object's title.
        If the object belongs to a series but the show_title flag is set to False, the method returns a list
        containing only the object's title and the volume label.
        Returns:
            list: A list containing the parts of the title.
        """
        if self.series and self.series.show_title:
            return [self.series.title, self.volume.label, self.title]
        return [self.title, self.volume.label] if self.belongs_to_series else [self.title]

    @property
    def full_title(self):
        """
        Returns the full title of the object.
        Returns:
            str: The full title of the object, composed by joining non-None parts with a hyphen.
        Example:
            'Part 1 - Part 2 - Part 3'
        """
        parts = [part for part in self._get_title_parts() if part is not None]
        return " - ".join(parts)

    @property
    def belongs_to_series(self):
        """
        Method: belongs_to_series
        Description:
        Returns True if the object belongs to a series, False otherwise.
        Parameters:
        - None
        Returns:
        - bool: True if the object belongs to a series, False otherwise.

        Examples:
        Example 1:
            obj = MyObject()
            assert obj.belongs_to_series() == False
        Example 2:
            obj.series = MySeries()
            assert obj.belongs_to_series() == True

        """
        return self.series is not None

    def _match_collection_attributes(self):
        """
        Update the attributes of the Collection object based on the attributes of the associated Series object.
        Parameters:
            self (Collection): The Collection object calling this method.
        Returns:
            None
        Note:
            This method is intended to be used internally and should not be called directly.
        """
        if self._title_is_empty:
            self.title = self.series.title
        self.author = self.series.author
        self.editor = self.series.editor
        self.audience = self.series.audience
        self.category = self.series.category
