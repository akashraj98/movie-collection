import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

def get_movies_from_api( page=1):
    url = f"{settings.MOVIE_API_URL}?page={page}"
    print(url)
    response = requests.get(url, auth=HTTPBasicAuth(settings.MOVIE_API_USERNAME, settings.MOVIE_API_PASSWORD),verify=False)
    if response.status_code == 200:
        return response.json()
    return None