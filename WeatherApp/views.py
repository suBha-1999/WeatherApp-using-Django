from django.shortcuts import render
from django.contrib import messages
import datetime
import requests

def home(request):
    # Get city from POST, default to 'salboni'
    city_name = request.POST.get('city', 'salboni')

    # OpenWeatherMap setup
    WEATHER_API_KEY = 'd9cf3d550a9f9dc08f36233194f9d9af'
    weather_url = f'https://api.openweathermap.org/data/2.5/weather'
    weather_params = {
        'q': city_name,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }

    # Google Custom Search API setup
    GOOGLE_API_KEY = 'AIzaSyDgCLkQ1R9UskQpKJtSCeixeeOV4pokAKQ'
    SEARCH_ENGINE_ID = '0273228923a354c58'
    query = city_name + " 1920x1080"
    image_url = None

    description = icon = temp = None
    exception_occurred = False

    # Fetch weather data
    try:
        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()

        if weather_response.status_code == 200 and 'main' in weather_data:
            description = weather_data['weather'][0]['description']
            icon = weather_data['weather'][0]['icon']
            temp = weather_data['main']['temp']
        else:
            raise KeyError
    except Exception:
        exception_occurred = True
        messages.error(request, 'Weather data not available for the entered city.')

    # Fetch image using Google Search API
    try:
        search_url = 'https://www.googleapis.com/customsearch/v1'
        search_params = {
            'key': GOOGLE_API_KEY,
            'cx': SEARCH_ENGINE_ID,
            'q': query,
            'searchType': 'image',
            'num': 1
        }
        image_response = requests.get(search_url, params=search_params)
        image_data = image_response.json()

        search_items = image_data.get('items', [])
        if search_items:
            image_url = search_items[0]['link']
        else:
            image_url = '/static/default.jpg'  # Optional fallback image
    except Exception:
        image_url = '/static/default.jpg'  # Fallback image

    # Render template
    return render(request, 'index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': datetime.date.today(),
        'city': city_name,
        'image_url': image_url,
        'exception_occurred': exception_occurred,
    })
