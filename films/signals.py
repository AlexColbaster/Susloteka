from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Director, Film, Genre, Log, Review


def write_log(message):
    Log.objects.create(info=message)


@receiver(post_save, sender=Film)
@receiver(post_save, sender=Director)
@receiver(post_save, sender=Review)
def log_model_save(sender, instance, created, **kwargs):
    action = 'Создан' if created else 'Изменён'
    write_log(f'{action} {sender._meta.verbose_name} ID: {instance.pk}')


@receiver(post_save, sender=Genre)
def log_genre_save(sender, instance, created, **kwargs):
    if created:
        write_log(f'Создан жанр ID: {instance.pk}')
    elif instance.is_deleted:
        write_log(f'Жанр мягко удалён, ID: {instance.pk}')
    else:
        write_log(f'Изменён жанр ID: {instance.pk}')


@receiver(post_delete, sender=Film)
@receiver(post_delete, sender=Director)
@receiver(post_delete, sender=Review)
def log_model_delete(sender, instance, **kwargs):
    write_log(f'Удалён {sender._meta.verbose_name} ID: {instance.pk}')


@receiver(post_delete, sender=Genre)
def log_genre_delete(sender, instance, **kwargs):
    write_log(f'Удалён жанр ID: {instance.pk}')
