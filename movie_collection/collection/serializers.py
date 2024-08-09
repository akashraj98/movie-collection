from rest_framework import serializers
from .models import Collection, Movie, CollectionMovie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']

class CollectionDetailSerializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']

    def get_movies(self, obj):
        collection_movies = CollectionMovie.objects.filter(collection=obj)
        return MovieSerializer([cm.movie for cm in collection_movies], many=True).data

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'uuid']

class CollectionMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionMovie
        fields = ['id', 'collection', 'movie']