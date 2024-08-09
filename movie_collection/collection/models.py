from django.db import models

from users.models import User
import uuid

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    genres = models.CharField(max_length=255, null=True, blank=True) # Comma-separated list of genres
    uuid = models.CharField(max_length=36, unique=True)

    def __str__(self):
        return self.title
    
class Collection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    uuid = models.CharField(max_length=36, unique=True,default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
from django.db import models

class CollectionMovie(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.collection.title} - {self.movie.title}'

