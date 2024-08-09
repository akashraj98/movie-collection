from django.http import JsonResponse
from rest_framework.views import APIView
from .service import get_movies_from_api
from rest_framework.permissions import IsAuthenticated
from .models import Collection, Movie, CollectionMovie
from rest_framework import status
from rest_framework.response import Response
from .serializers import CollectionSerializer

class MovieListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        page = request.GET.get('page', 1)
        movies_data = get_movies_from_api(page)
        if movies_data is not None:
            # change the next and previous url accordingly
            return JsonResponse(movies_data)
        else:
            return JsonResponse({'error': 'Failed to fetch movies'}, status=500)
        

class CollectionListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
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
        return Response({
            "is_success": True,
            "data": {
                "collections": serializer.data,
                "favourite_genres": ", ".join(top_genres)
            }
        })
    
    def post(self, request):
        data = request.data
        title = data.get('title')
        description = data.get('description')
        user = request.user
        collection_obj, created = Collection.objects.get_or_create(
            title=title,
            description=description,
            user = user
        )

        movies = data.get('movies')
        for movie in movies:
            try:
                movie_obj = Movie.objects.get(uuid=movie['uuid'])
            except Movie.DoesNotExist:
                movie_obj = Movie.objects.create(
                    title=movie['title'],
                    description=movie['description'],
                    genres=movie['genres'],
                    uuid=movie['uuid']
                )

            CollectionMovie.objects.create(
                collection=collection_obj,
                movie=movie_obj
            )
        return Response({
            "is_success": True,
            "message": "Collection created successfully",
            "collection_uuid": collection_obj.uuid

        },status=status.HTTP_201_CREATED)
            

    
class CollectionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        try:
            collection = Collection.objects.get(uuid=uuid, user=request.user)
        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def put(self, request, uuid):
        try:
            collection = Collection.objects.get(uuid=uuid, user=request.user)
        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        try:
            collection = Collection.objects.get(uuid=uuid, user=request.user)
        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)

        collection.delete()
        return Response({"message": "Collection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)