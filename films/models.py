from django.db import models
from django.db.models import Avg
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video = models.FileField(
        upload_to='films/videos/',
        validators=[FileExtensionValidator(['mp4', 'mkv', 'mov', 'webm'])],
    )
    genres = models.ManyToManyField(Genre, related_name='films', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

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
    author = models.CharField(max_length=80)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author} - {self.film.title}'
