from django.db import migrations


def create_genres(apps, schema_editor):
    Genre = apps.get_model('films', 'Genre')
    for name in [
        'Драма',
        'Комедия',
        'Боевик',
        'Триллер',
        'Фантастика',
        'Ужасы',
        'Романтика',
        'Приключения',
        'Анимация',
        'Документальный',
    ]:
        Genre.objects.get_or_create(name=name)


def remove_genres(apps, schema_editor):
    Genre = apps.get_model('films', 'Genre')
    Genre.objects.filter(name__in=[
        'Драма',
        'Комедия',
        'Боевик',
        'Триллер',
        'Фантастика',
        'Ужасы',
        'Романтика',
        'Приключения',
        'Анимация',
        'Документальный',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_genres, remove_genres),
    ]
