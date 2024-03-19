import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Book, Collection


@receiver(pre_delete, sender=Book)
def delete_book_img_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_delete, sender=Collection)
def delete_collection_img_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


def auto_delete_img_on_change(model, instance, **kwargs):
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
    auto_delete_img_on_change(sender, instance, **kwargs)


@receiver(pre_save, sender=Collection)
def auto_delete_collection_img_on_change(sender, instance, **kwargs):
    auto_delete_img_on_change(sender, instance, **kwargs)


@receiver(pre_save, sender=Book)
def auto_set_data_on_save(sender, instance, **kwargs):
    """
    Auto set data when book is published
    """
    if instance.published:
        instance.current_reading = False
        instance.incoming_reading = False
        obj = Book.objects.filter(pk=instance.pk).first()
        if (obj and not obj.published) or not obj:
            instance.published_at = timezone.now()

    if instance.current_reading:
        current_books = Book.objects.filter(current_reading=True)
        for book in current_books:
            book.current_reading = False
            book.save()
