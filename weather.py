import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

#with open('country.json','r') as f:
    #place_dict = json.load(f)
#place = json.loads(place_dict)['country']

#place = 'oslo'


def get_current_weather(location):

    '''Function makes an API call to the weather API
    
    Args:
        location: location for which you want the weather'''

    api_key = WEATHER_API_KEY
    
    url = 'http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no'
    url = url.format(api_key, location)

    response = requests.get(url)
    data = response.json()
    return data

#data = get_current_weather('norway')
#print(data)