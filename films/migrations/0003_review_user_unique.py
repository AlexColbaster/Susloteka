from django.conf import settings
from django.db import migrations, models


def attach_review_users(apps, schema_editor):
    Review = apps.get_model('films', 'Review')
    User = apps.get_model('auth', 'User')

    users_by_username = {user.username: user for user in User.objects.all()}
    seen = set()

    for review in Review.objects.order_by('created_at', 'id'):
        user = users_by_username.get(review.author)
        if user is None:
            continue

        key = (review.film_id, user.id)
        if key in seen:
            review.user = None
        else:
            review.user = user
            seen.add(key)
        review.save(update_fields=['user'])


def detach_review_users(apps, schema_editor):
    Review = apps.get_model('films', 'Review')
    Review.objects.update(user=None)


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_seed_genres'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name='film_reviews',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(attach_review_users, detach_review_users),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('film', 'user'), name='unique_review_per_film_user'),
        ),
    ]
