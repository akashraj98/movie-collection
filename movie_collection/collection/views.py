from django.http import JsonResponse
from rest_framework.views import APIView
from .services import get_movies_from_api
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from . import services

class MovieListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        page = request.GET.get('page', 1)
        movies_data = get_movies_from_api(page)
        if movies_data is not None:
            return JsonResponse(movies_data)
        else:
            return JsonResponse({'error': 'Failed to fetch movies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CollectionListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        result = services.get_user_collections(request.user)
        return Response(result, status=status.HTTP_200_OK)
    
    def post(self, request):
        result = services.create_collection(request.user, request.data)
        return Response(result, status=status.HTTP_201_CREATED)

class CollectionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        result = services.get_collection_detail(request.user, uuid)
        if result is None:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        result = services.update_collection(request.user, uuid, request.data)
        if result is None:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)
        if 'errors' in result:
            return Response(result['errors'], status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request, uuid):
        result = services.delete_collection(request.user, uuid)
        if not result:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Collection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)