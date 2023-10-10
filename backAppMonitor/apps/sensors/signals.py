import os
from django.conf import settings
from django.db.models.signals import pre_save, post_delete
from .models import Device, Located
from django.dispatch import receiver


# Eliminar imagenes al momento de borrar registro
@receiver(post_delete, sender=Device)
def delete_image_signal_device(sender, instance, **kargs):
    if instance.imagen_device:
        if os.path.isfile(instance.imagen_device.path):
            os.remove(instance.imagen_device.path)

    (root, ext) = os.path.splitext(instance.imagen_device.path)

    extra_file = root + ".option" + ext

    if os.path.isfile(extra_file):
        os.remove(extra_file)


@receiver(post_delete, sender=Located)
def delete_image_signal_located(sender, instance, **kargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

    (root, ext) = os.path.splitext(instance.image.path)

    extra_file = root + ".option" + ext

    if os.path.isfile(extra_file):
        os.remove(extra_file)


# Eliminar imagenes al momento de actualizar registro
@receiver(pre_save, sender=Device)
def change_image_signal_device(sender, instance, **kargs):
    if not instance.pk:
        return False

    try:
        old_file = Device.objects.get(pk=instance.pk).imagen_device
        (root, ext) = os.path.splitext(old_file.path)
        old_extra_file = root + ".option" + ext
    except Device.DoesNotExist:
        return False

    new_file = instance.imagen_device

    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

        if os.path.isfile(old_extra_file):
            os.remove(old_extra_file)


@receiver(pre_save, sender=Located)
def change_image_signal_located(sender, instance, **kargs):
    if not instance.pk:
        return False

    try:
        old_file = Located.objects.get(pk=instance.pk).image
        (root, ext) = os.path.splitext(old_file.path)
        old_extra_file = root + ".option" + ext
    except Located.DoesNotExist:
        return False

    new_file = instance.image

    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

        if os.path.isfile(old_extra_file):
            os.remove(old_extra_file)
