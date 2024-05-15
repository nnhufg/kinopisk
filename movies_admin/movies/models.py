from django.db import models
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

ROLE_CHOICES = [
        ('actor', _('Actor')),
        ('director', _('Director')),
        ('writer', _('Writer')),
]

class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Filmwork(UUIDMixin, TimeStampedMixin):

    title = models.TextField(_('title'))
    description = models.TextField(_('description'), blank=True, default="Нет описания")
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    rating = models.FloatField(_('rating'), blank=True, null=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.TextField(_('type'))
    file_path = models.TextField(_('file_path'), blank=True, default="")

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Film')
        verbose_name_plural = _('Films')


class Genre(UUIDMixin, TimeStampedMixin):

    name = models.TextField(_('name'))
    description = models.TextField(_('description'), blank=True, default="")


    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres' )


class Person(UUIDMixin, TimeStampedMixin):

    full_name = models.TextField(_('full_name'))

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons' )


class GenreFilmWork(UUIDMixin, TimeStampedMixin):

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('film'))
    genre = models.ForeignKey(Genre, models.CASCADE, verbose_name=_('genre'))

    class Meta:
        db_table = "content\".\"genre_film_work"
        unique_together = (('film_work', 'genre'),)
        verbose_name = _('Genre-Film')
        verbose_name_plural = _('Genres-Films')


class PersonFilmWork(UUIDMixin, TimeStampedMixin):

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('film'))
    person = models.ForeignKey(Person, models.CASCADE, verbose_name=_('person'))
    role = models.TextField(_('role'), blank=True, choices=ROLE_CHOICES, default="")

    class Meta:
        db_table = "content\".\"person_film_work"
        unique_together = (('film_work', 'person'),)
        verbose_name = _('Person-Film')
        verbose_name_plural = _('Persons-Films')