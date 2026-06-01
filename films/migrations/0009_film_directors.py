from django.db import migrations, models


def copy_director_to_directors(apps, schema_editor):
    Film = apps.get_model('films', 'Film')
    for film in Film.objects.all():
        director_id = getattr(film, 'director_id', None)
        if director_id:
            film.directors.add(director_id)


def copy_directors_to_director(apps, schema_editor):
    Film = apps.get_model('films', 'Film')
    for film in Film.objects.all():
        first_director = film.directors.first()
        if first_director:
            film.director_id = first_director.id
            film.save(update_fields=['director'])


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0008_alter_director_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='directors',
            field=models.ManyToManyField(blank=True, related_name='films', to='films.director'),
        ),
        migrations.RunPython(copy_director_to_directors, copy_directors_to_director),
        migrations.RemoveField(
            model_name='film',
            name='director',
        ),
    ]
