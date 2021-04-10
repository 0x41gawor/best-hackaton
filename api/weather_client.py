import requests
import json


'''
Args: string -'miasto, kraj'
      int - prognoza za ile godzin
Return: (temperatura, zachmurzenie) 
'''
def get_weather(city, hours):
    url = "https://community-open-weather-map.p.rapidapi.com/forecast"
    querystring = {"q":city,"units":"metric"}

    headers = {
    'x-rapidapi-key': "6a85af24aemsh106af2e327578f0p10f7afjsnd281b984835f",
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_res = json.loads(response.text)
    hour_interval = int(hours/3)

    weather_at_interval = json_res['list'][hour_interval]
    temp = weather_at_interval['main']['temp']
    clouds = weather_at_interval['clouds']['all']

    return (temp, clouds)

