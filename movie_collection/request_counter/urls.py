from django.urls import path
from .views import * 
urlpatterns = [
    path('request-count/', RequestCountView.as_view(), name='get_request_count'),
    path('request-count/reset/', RequestCountResetView.as_view(), name='reset_request_count'),
]