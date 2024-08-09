import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from .models import Collection, Movie, CollectionMovie
from .serializers import CollectionSerializer, CollectionDetailSerializer, MovieSerializer

def get_movies_from_api( page=1):
    url = f"{settings.MOVIE_API_URL}?page={page}"
    print(url)
    response = requests.get(url, auth=HTTPBasicAuth(settings.MOVIE_API_USERNAME, settings.MOVIE_API_PASSWORD),verify=False)
    if response.status_code == 200:
        return response.json()
    return None


def get_user_collections(user):
    collections = Collection.objects.filter(user=user)
    serializer = CollectionSerializer(collections, many=True)
    
    genre_counts = {}
    for collection in collections:
        movies = CollectionMovie.objects.filter(collection=collection)
        for movie in movies:
            for genre in movie.movie.genres.split(','):
                genre = genre.strip()
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_genres = [genre for genre, _ in top_genres]
    
    return {
        "is_success": True,
        "data": {
            "collections": serializer.data,
            "favourite_genres": ", ".join(top_genres)
        }
    }

def create_collection(user, data):
    title = data.get('title')
    description = data.get('description')
    collection_obj, created = Collection.objects.get_or_create(
        title=title,
        description=description,
        user=user
    )

    movies = data.get('movies', [])
    for movie in movies:
        movie_obj, _ = Movie.objects.get_or_create(
            uuid=movie['uuid'],
            defaults={
                'title': movie['title'],
                'description': movie['description'],
                'genres': movie['genres'],
            }
        )
        CollectionMovie.objects.create(collection=collection_obj, movie=movie_obj)

    return {
        "is_success": True,
        "message": "Collection created successfully",
        "collection_uuid": collection_obj.uuid
    }

def get_collection_detail(user, uuid):
    try:
        collection = Collection.objects.get(uuid=uuid, user=user)
    except Collection.DoesNotExist:
        return None
    serializer = CollectionDetailSerializer(collection)
    return serializer.data

def update_collection(user, uuid, data):
    try:
        collection = Collection.objects.get(uuid=uuid, user=user)
    except Collection.DoesNotExist:
        return None

    serializer = CollectionDetailSerializer(collection, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        if 'movies' in data:
            CollectionMovie.objects.filter(collection=collection).delete()
            movie_data = data['movies']
            for movie_item in movie_data:
                movie_serializer = MovieSerializer(data=movie_item)
                if movie_serializer.is_valid():
                    movie, created = Movie.objects.get_or_create(
                        uuid=movie_serializer.validated_data['uuid'],
                        defaults=movie_serializer.validated_data
                    )
                    CollectionMovie.objects.create(collection=collection, movie=movie)
                else:
                    return {'errors': movie_serializer.errors}

        updated_serializer = CollectionDetailSerializer(collection)
        return updated_serializer.data
    return {'errors': serializer.errors}

def delete_collection(user, uuid):
    try:
        collection = Collection.objects.get(uuid=uuid, user=user)
    except Collection.DoesNotExist:
        return False
    collection.delete()
    return True