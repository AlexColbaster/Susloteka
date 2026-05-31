from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from .models import Film, Genre, Review


try:
    admin.site.unregister(User)
except NotRegistered:
    pass


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
