from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bs4 import BeautifulSoup
import requests
import urllib
import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime

def index(request):
    return HttpResponse("Scraping!")

@api_view(['GET'])
def scrap(request):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://dota2.ru/forum/forums/obschie-voprosy-i-obsuzhdenija.5/'
    # url = 'https://tgstat.com/ru'

    req = requests.get(url, headers=headers).text
    soup = BeautifulSoup(req, 'lxml')

    ads = soup.find_all('div', class_ = 'forum-section__title')
    for i in range(len(ads)):
        print(ads[i].find('a').text)
        
    return Response({"done!"})
