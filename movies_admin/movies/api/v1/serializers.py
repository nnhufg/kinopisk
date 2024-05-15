from rest_framework import serializers 
from movies.models import Filmwork


class FilmworkSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()

    class Meta:
        model = Filmwork
        fields = ['id', 'title', 'description', 'creation_date', 'rating', 'type', 'genres', 'actors', 'directors', 'writers']

    def get_genres(self, filmwork):
        genres = filmwork.genrefilmwork_set.all().prefetch_related('genre')
        return [genre.genre.name for genre in genres]

    def get_persons(self, filmwork, role):
        persons = filmwork.personfilmwork_set.filter(role=role).prefetch_related('person')
        return [person.person.full_name for person in persons]

    def get_actors(self, filmwork):
        return self.get_persons(filmwork, role='actor')

    def get_directors(self, filmwork):
        return self.get_persons(filmwork, role='director')

    def get_writers(self, filmwork):
        return self.get_persons(filmwork, role='writer')