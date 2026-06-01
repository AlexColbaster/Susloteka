from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0004_director_film_director'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='link',
            field=models.URLField(blank=True),
        ),
    ]
