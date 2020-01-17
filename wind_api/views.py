from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from wind_api.serializers import UserSerializer, ObservationSerializer
from django_filters.rest_framework import DjangoFilterBackend
import os
import csv
import requests
import json
import urllib
import aiohttp
import asyncio
from wind_api.models import Observation, APItoken, ElementsReturned, Localization
from django_filters import rest_framework as filters
from django.shortcuts import render_to_response
from rest_framework.pagination import PageNumberPagination

def index(request):
    # return HttpResponse('<html><head><title>WIND API</title></head><p>Click the button to open a new browser window.</p><button onclick="myFunction()">Try it</button><script> function myFunction() { window.location("https://www.w3schools.com"); } </script></html>')
    return render_to_response('index.html')

def getObservations(request):

    # Dropping records from database
    Observation.objects.all().delete()

    localizations = Localization.objects.all().filter(capital__contains="primary")
    list_of_urls = []

    for city in localizations:

        # Just for test purposes. Data pull from another API (allowing to make more requests per 24h)
        '''
        first = 'http://api.aerisapi.com/observations/closest?p='
        lat = city[1]
        lon = city[2]
        last = '&client_id=ByruDorHEne2JB64BhP1k&client_secret=Jp4xullRcy6DXTPSTKBGXAvGGTaT04iiUQXPj0ob'

        url = first + str(lat) + ',' + str(lon) + last
        list_of_urls.append(url)
        '''

        # https://api.weatherbit.io/v2.0/current?lat=38.9047&lon=-77.0163&key=87440aed6e82411eb182a15f12d9d645
        first = 'https://api.weatherbit.io/v2.0/current?lat='
        lat = city.latitude
        connector = '&lon='
        lon = city.longitude
        last = '&key='

        # Set the token in admin dashboard: 'http://localhost:8000/admin/wind_api/apitoken/'
        # Free user is allowet to make only 1000 requests per 24h. Unfortunately you need to get new token after every 4 data updates.
        token = APItoken.objects.get(id=1).token

        url = first + str(lat) + connector + str(lon) + last + token
        list_of_urls.append(url)

    list = []

    # Asynchronyous data pull
    async def fetch(session, url):
        async with session.get(url) as response:
            # list.append(response.content.read(1024))
            async for line in response.content:
                list.append(line.decode('utf-8'))
            return await response.release()


    async def main(loop):

        urls = list_of_urls

        async with aiohttp.ClientSession(loop=loop) as session:
            resp = [fetch(session, url) for url in urls]
            await asyncio.gather(*resp)

    # loop = asyncio.get_event_loop()
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))
    loop.close()

    bulk_list = []

    # Creating objects from data pulled from API weatherbit.io
    for i in list:
        i = json.loads(i)
        print(i)
        observation_time = i['data'][0]['ob_time']
        country_code = i['data'][0]['country_code']
        city_name = i['data'][0]['city_name']
        latitude = i['data'][0]['lat']
        longitude = i['data'][0]['lon']
        wind_speed = i['data'][0]['wind_spd']
        wind_direction_full = i['data'][0]['wind_cdir_full']
        wind_direction_short = i['data'][0]['wind_cdir']
        wind_direction_degrees = i['data'][0]['wind_dir']

        bulk_object = Observation(observation_time=observation_time, country_code=country_code, city_name=city_name, latitude=latitude, longitude=longitude, wind_speed=wind_speed, wind_direction_full=wind_direction_full, wind_direction_short=wind_direction_short, wind_direction_degrees=wind_direction_degrees)
        bulk_list.append(bulk_object)

    # Bulk insert to database
    Observation.objects.bulk_create(bulk_list)

    return HttpResponse('<p>Fresh data is already in the database. Feel free to play with API</p>')

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class PaginationModifier(PageNumberPagination):

    page_size = ElementsReturned.objects.get(id=1).elements
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ObservationFilter(filters.FilterSet):

    class Meta:
        model = Observation
        fields = ['wind_direction_short', 'wind_direction_full']

class ObservationViewSet(viewsets.ModelViewSet):

    queryset = Observation.objects.all().order_by('-wind_speed')
    serializer_class = ObservationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ObservationFilter
    pagination_class = PaginationModifier
    http_method_names = ['get']

def getLocalizations(request):

    Localization.objects.all().delete()
    # Download world-cities file first and put it to some free file sherign service, for example: gofile.io
    url= 'https://srv-file4.gofile.io/download/LkffsQ/worldcities.csv'

    # Locations download and insert into database; source: https://simplemaps.com/data/world-cities
    response = urllib.request.urlopen(url)
    data = response.read()
    data = data.decode('utf-8')
    data = data.split('\r\n')
    cities = []
    for d in data:
        d = d.replace('"', '')
        d = d.split(',')
        cities.append(d)

    del cities[0]
    del cities[-1]

    bulk_localizations = []
    temp_localizations = []
    for c in cities:
        temp_loc = []
        temp_object = Localization(city_name=c[0], latitude=c[2], longitude=c[3], country=c[4], country_code=c[5], capital=c[8])
        temp_loc = [c[0], c[2], c[3], c[4], c[5], c[8]]

        if temp_loc not in temp_localizations:
            bulk_localizations.append(temp_object)

        temp_localizations.append(temp_loc)

    Localization.objects.bulk_create(bulk_localizations)
    return HttpResponse('<p>Locations added to database</p>')

def test(request):

    localizations = Localization.objects.all().filter(capital__contains="primary")
    for i in localizations:
        print(i)

    return HttpResponse('<p>Test status: OK</p>')
