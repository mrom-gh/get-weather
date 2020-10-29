#!/usr/bin/python3
#
# get_weather.py - Prints the weather for a location from the
# command line.

import sys, requests, json, datetime
APPID = str(sys.argv[1])

# Compute location from command line arguments.
if len(sys.argv) < 3:
    print('Usage: get_open_weather.py APPID city_name, 2-letter_country_code')
    sys.exit()
location = ' '.join(sys.argv[2:])

# 1) Current weather API - needed to get coordinates from City name / zip code
url = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s' % (location, APPID)
response = requests.get(url)
response.raise_for_status()
s_current = response.text
d_current = json.loads(s_current)
lon, lat = d_current['coord']['lon'], d_current['coord']['lat']

# 2) One Call API (current weather; minutely, hourly, daily forecasts; historic weather)
url =  'https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s' % (str(lat),str(lon), APPID)
response = requests.get(url)
response.raise_for_status()
s_onecall = response.text
d_onecall = json.loads(s_onecall)

# Define print functions for current weather and daily forecasts
def print_sun_times(d):
    sunrise = datetime.datetime.fromtimestamp(
        d['sunrise']
        ).strftime('%H:%M:%S')
    sunset = datetime.datetime.fromtimestamp(
        d['sunset']
        ).strftime('%H:%M:%S')
    print('  Sunrise:', sunrise, '- Sunset:', sunset)

def print_current_weather(d_current, location, lon, lat):
    print(datetime.datetime.fromtimestamp(d_current['dt']).strftime('%Y-%m-%d %H:%M:%S'), '\n')
    weather = d_current['weather']
    print('Current weather in %s' % (location), '(%g %g):' % (lon, lat))
    print(' ', weather[0]['main'], '-', weather[0]['description'])
    temp = d_current['main']
    print('  Temperature:', round(temp['temp']-273.15, 1), '°C')
    print_sun_times(d_current['sys'])
    print()

def print_daily_weather(d_onecall, i):
    daily = d_onecall['daily']
    day = ['Today', 'Tomorrow', 'Day after tomorrow']
    print('%s:' % day[i])
    print(' ', daily[i]['weather'][0]['main'], '-', daily[i]['weather'][0]['description'])
    temp = daily[i]['temp']
    print('  Temperature:', round(temp['day']-273.15, 1), '°C')
    #print_sun_times(daily[i])
    print()

# Print current weather and daily forecasts
print_current_weather(d_current, location, lon, lat)
for i in range(3):
    print_daily_weather(d_onecall, i)