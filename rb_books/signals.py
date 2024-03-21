import os

from django.db.models.signals import pre_delete, pre_save, post_migrate
from django.dispatch import receiver
from django.utils import timezone

from .models import Book, Series, Volume


@receiver(post_migrate)
def populate_volumes(sender, **kwargs):
    """
    Populates volumes in the Volume database table after a migration for the 'rb_books' app.
    Parameters:
    - sender: The sender of the post_migrate signal.
    - **kwargs: Additional keyword arguments.
    Return Type:
    - None
    Example Usage:
    populate_volumes(sender, **kwargs)
    """
    if sender.name == 'rb_books' and not Volume.objects.exists():
        for index in [x * 0.5 for x in range(2, 41)] + [x for x in range(21, 151)]:
            str_index = str(index)
            new_volume = Volume.objects.create(
                label=f"Tome {str_index[:-2] if str_index.endswith('.0') else str_index}",
                index=index
            )
            print(f'{new_volume.label} saved into Volume database table')


@receiver(pre_delete, sender=Book)
def delete_book_img_file(sender, instance, **kwargs):
    """
    Delete the image file associated with a book before the book is deleted.
    @param sender: The sender object.
    @param instance: The book instance being deleted.
    @param kwargs: Additional keyword arguments.
    @return: None
    @receiver(pre_delete, sender=Book)
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_delete, sender=Series)
def delete_collection_img_file(sender, instance, **kwargs):
    """
    Deletes the collection image file associated with the given instance of a Series model.
    Parameters:
    - sender: The sender of the pre_delete signal. It should be a Series model.
    - instance: The instance of the Series model about to be deleted.
    Returns:
    None
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


def auto_delete_img_on_change(model, instance, **kwargs):
    """
    Automatically deletes the old image file when the image field is changed on a model instance.
    Parameters:
    - model: The model class to identify the model instance.
    - instance: The model instance to check for changes and delete the old image file.
    - kwargs: Additional keyword arguments (if any).
    Returns:
    - None
    Example Usage:
    auto_delete_img_on_change(MyModel, my_instance)
    """
    if instance.pk:
        try:
            old_instance = model.objects.get(pk=instance.pk)
        except model.DoesNotExist:
            return
        old_file = old_instance.image
        new_file = instance.image
        if bool(old_file) and old_file != new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)


@receiver(pre_save, sender=Book)
def auto_delete_collection_img_on_change(sender, instance, **kwargs):
    """
    This method is a receiver function that is triggered before saving a Book instance. It is used to automatically
    delete collection images when there is a change.
    Parameters:
    - sender: The sender of the signal.
    - instance: The instance of the Book class being saved.
    - kwargs: Additional keyword arguments.
    Returns: None
    Note: This method is called by the `pre_save` signal with the `sender` parameter set to `Book`. It internally calls
     the `auto_delete_img_on_change` method passing the same arguments
    * received by this function.
    Example Usage:
    @receiver(pre_save, sender=Book)
    def auto_delete_collection_img_on_change(sender, instance, **kwargs):
        auto_delete_img_on_change(sender, instance, **kwargs)
    """
    auto_delete_img_on_change(sender, instance, **kwargs)


@receiver(pre_save, sender=Series)
def auto_delete_collection_img_on_change(sender, instance, **kwargs):
    """
    This method is a signal receiver function that is triggered before saving an instance of the "Series" model.
    Parameters:
    - sender: the model class that is sending the signal (Series in this case)
    - instance: the specific instance of the model being saved
    - **kwargs: additional keyword arguments
    Return Type:
    None
    This method acts as a wrapper and simply calls the "auto_delete_img_on_change" function, passing the same
    parameters. The purpose of this function is to automatically delete the collection
    * image associated with the series if any changes are made to it.
    """
    auto_delete_img_on_change(sender, instance, **kwargs)


@receiver(pre_save, sender=Book)
def auto_set_data_on_save(sender, instance, **kwargs):
    """
    This method, `auto_set_data_on_save`, is a receiver for the `pre_save` signal with the sender as `Book`. It
    automatically sets certain data on the instance of `Book` before saving it
    *.
    Parameters:
    - `sender`: The sender of the signal.
    - `instance`: The instance of the `Book` model that is being saved.
    - `**kwargs`: Additional keyword arguments passed to the receiver.
    Return Type: None
    When the `instance` has the `published` field set to True:
    - The `current_reading` field of the `instance` is set to False.
    - The `incoming_reading` field of the `instance` is set to False.
    - If the `published_at` field of the `instance` is None, it is set to the current time using `timezone.now()`.
    When the `instance` has the `current_reading` field set to True:
    - If the `incoming_reading` field of the `instance` is also True, it is set to False.
    - All other `Book` instances with `current_reading` set to True are iterated over and their `current_reading`
    field is set to False, and each instance is saved.
    Note: This method should be connected as a receiver to the `pre_save` signal for the `Book` model in order for it
    to be automatically triggered before saving a `Book` instance
    """
    if instance.published:
        instance.current_reading = False
        instance.incoming_reading = False
        if instance.published_at is None:
            instance.published_at = timezone.now()

    if instance.current_reading:
        if instance.incoming_reading:
            instance.incoming_reading = False
        current_books = Book.objects.filter(current_reading=True)
        for book in current_books:
            book.current_reading = False
            book.save()
