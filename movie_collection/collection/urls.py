from django.urls import path
from .views import *


urlpatterns = [
    path('', CollectionListCreateView.as_view(), name='collection-list-create'),
    path('<str:uuid>', CollectionDetailView.as_view(), name='collection-detail'),

]