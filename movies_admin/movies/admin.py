from django.contrib import admin
from .models import *


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 0


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 0


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = ('title', 'description', 'creation_date', 'rating', 'type', 'created', 'modified')
    list_filter = ('type', 'creation_date', 'rating')
    search_fields = ('title', 'creation_date',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    list_filter = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    search_fields = ('full_name', )


@admin.register(GenreFilmWork)
class GenreFilmWorkAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'genre', 'created', 'modified')
    search_fields = ('film_work__title', 'genre__name',)


@admin.register(PersonFilmWork)
class PersonFilmWorkAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'person', 'role', 'created', 'modified')
    search_fields = ('film_work__title', 'person__full_name', 'role')
