from django.contrib import admin

from .models import Film, Genre, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['genres', 'created_at']
    filter_horizontal = ['genres']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['film', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['author', 'text', 'film__title']
