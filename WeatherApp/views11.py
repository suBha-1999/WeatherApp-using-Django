from django.shortcuts import render
from django.contrib import messages
import datetime
import requests

# Create your views here.
def home(request):
    # Get city name from POST, default to 'salboni'
    city_name = request.POST.get('city', 'salboni')

    url= f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=d9cf3d550a9f9dc08f36233194f9d9af'
    prm = {'units' : 'metric'}

    API_KEY = 'AIzaSyDgCLkQ1R9UskQpKJtSCeixeeOV4pokAKQ'
    SEARCH_ENGINE_ID = '0273228923a354c58'

    QUERY = city_name + "1920*1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={QUERY}&start={start}&searchType={searchType}"


    data = requests.get(city_url).json()
    count = 1
    search_items = data.get("items")
    image_url = search_items[1]['link']

    try:
        data = requests.get(url, prm).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'index.html',
                    {'description':description,
                    'icon':icon,
                    'temp':temp,
                    'day':day,
                    'city':city_name,
                    'exception_occurred' : False,
                    'image_url':image_url
                    })
    except KeyError:
        exception_occurred = True
        messages.error(request, 'Entered data not available')
        day = datetime.date.today()
        return render(request, 'index.html',
                    {'description':description,
                    'icon':icon,
                    'temp':temp,
                    'day':day,
                    'city':city_name,
                    })
