import requests
from django.shortcuts import render

from .forms import CityForm
from .models import City


def index(request):
    url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&appid=2c76c469896544c20c6224f4ab128f53'
    urllatlon = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=2c76c469896544c20c6224f4ab128f53'

    cities = City.objects.all()  # return all the cities in the database

    if request.method == 'POST':  # only true if form is submitted
        form = CityForm(request.POST)  # add actual request data to form for processing
        form.save()  # will validate and save if validate

    form = CityForm()

    weather_data = []
    for city in cities:
        # get latitude and longitude of the city
        get_lat_lon = requests.get(
            url.format(city)).json()  # request the API data and convert the JSON to Python data types

        latlong = {
            'name': get_lat_lon[0]['name'],
            'lat': get_lat_lon[0]['lat'],
            'long': get_lat_lon[0]['lon']
        }

        city_weather = requests.get(urllatlon.format(latlong['lat'], latlong['long'])).json()

        weather = {
            'city': city_weather['name'],
            'condition': city_weather['weather'][0]['main'],
            'temperature': city_weather['main']['temp'],
            'icon': city_weather['weather'][0]['icon'],
        }
        weather_data.append(weather)

    context = {
        'weather_data': weather_data,
        'form': form
    }

    return render(request, 'weather/index.html', context)
