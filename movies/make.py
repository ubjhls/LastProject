import os
import sys
import urllib.request
import requests

response = requests.get('https://api.themoviedb.org/3/movie/11?api_key=1dfd52c8a24a0f38f40efe41c86be13b&language=ko-KR').json()
print(response)