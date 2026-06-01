from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.urls import path, reverse

from .models import Director, Film, Genre, Review


try:
    admin.site.unregister(User)
except NotRegistered:
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_url'] = reverse('export_table', args=['genres'])
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']
    search_fields = ['name', 'description', 'link']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_url'] = reverse('export_table', args=['directors'])
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'director_list', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['directors', 'genres', 'created_at']
    filter_horizontal = ['genres', 'directors']

    def director_list(self, obj):
        return ', '.join(director.name for director in obj.directors.all()) or 'Не указан'

    director_list.short_description = 'Режиссёры'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_url'] = reverse('export_table', args=['films'])
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['film', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['author', 'text', 'film__title']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_url'] = reverse('export_table', args=['reviews'])
        return super().changelist_view(request, extra_context=extra_context)


def _librarian_group():
    group, _ = Group.objects.get_or_create(name='librarian')
    return group


@admin.action(description='Сделать библиотекарем')
def make_librarian(modeladmin, request, queryset):
    group = _librarian_group()
    for user in queryset:
        user.groups.add(group)


@admin.action(description='Убрать права библиотекаря')
def remove_librarian(modeladmin, request, queryset):
    group = _librarian_group()
    for user in queryset:
        user.groups.remove(group)


class UserAdmin(BaseUserAdmin):
    actions = [make_librarian, remove_librarian]
    list_display = BaseUserAdmin.list_display + ('is_librarian',)

    def is_librarian(self, obj):
        return obj.is_superuser or obj.groups.filter(name='librarian').exists()

    is_librarian.boolean = True
    is_librarian.short_description = 'Библиотекарь'


try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, UserAdmin)
