from rest_framework import serializers
from movies.models import *


class FilmworkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Filmwork
        fields = '__all__'

