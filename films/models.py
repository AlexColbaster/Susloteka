from django.db import models
from django.db.models import Avg
from django.db.models import Q
from django.conf import settings
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField('имя', max_length=120, unique=True)
    description = models.TextField('описание', blank=True)
    link = models.URLField('ссылка', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'режиссёр'
        verbose_name_plural = 'режиссёры'

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=200)
    directors = models.ManyToManyField(Director, related_name='films', blank=True)
    description = models.TextField()
    video = models.FileField(
        upload_to='films/videos/',
        validators=[FileExtensionValidator(['mp4', 'mkv', 'mov', 'webm'])],
    )
    genres = models.ManyToManyField(Genre, related_name='films', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'фильм'
        verbose_name_plural = 'фильмы'

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        result = self.reviews.aggregate(value=Avg('rating'))['value']
        return round(result, 1) if result is not None else None

    @property
    def reviews_count(self):
        return self.reviews.count()


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='film_reviews',
    )
    author = models.CharField(max_length=80)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['film', 'user'], name='unique_review_per_film_user'),
            models.CheckConstraint(condition=Q(rating__gte=1, rating__lte=10), name='review_rating_1_10'),
        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return f'{self.author} - {self.film.title}'
