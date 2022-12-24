from django.conf import settings
import requests
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.decorators import api_view


@api_view(["POST"])
def getweather(request):
    city = request.data.get("city")
    country = request.data.get("country")

    key = settings.WEATHER_API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}".format(city,country,key)

    city_weather = requests.get(url).json()
    print(city_weather)
    if city_weather.keys():
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
        }
        return Response(
            weather,
            status=HTTP_200_OK
        )
    else:
        return Response(
            {'status': 'Check city name and country code'},
            status=HTTP_404_NOT_FOUND
        )
