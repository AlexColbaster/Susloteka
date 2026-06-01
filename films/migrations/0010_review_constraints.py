from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0009_film_directors'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(
                condition=Q(rating__gte=1, rating__lte=10),
                name='review_rating_1_10',
            ),
        ),
    ]
