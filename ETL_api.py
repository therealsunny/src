
from datetime import datetime as dt
import requests
import pandas as pd


def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return round(temp_in_fahrenheit, 2)

def transform_weather_data(weather_data):
    city = weather_data['name']
    weather_description = weather_data['weather'][0]['description']
    temp_fahrenheit = kelvin_to_fahrenheit(weather_data['main']['temp'])
    feels_like_fahrenheit = kelvin_to_fahrenheit(weather_data['main']['feels_like'])
    min_temp_fahrenheit = kelvin_to_fahrenheit(weather_data['main']['temp_min'])
    max_temp_fahrenheit = kelvin_to_fahrenheit(weather_data['main']['temp_max'])
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    time_of_record = dt.fromtimestamp(weather_data['dt'] + weather_data['timezone'])
    sunrise_time = dt.fromtimestamp(weather_data['sys']['sunrise'] + weather_data['timezone'])
    sunset_time = dt.fromtimestamp(weather_data['sys']['sunset'] + weather_data['timezone'])

    transformed_weather_data = {
        'City': city,
        'Description': weather_description,
        'Temperature (F)': temp_fahrenheit,
        'Feels Like (F)': feels_like_fahrenheit,
        'Minimum Temperature (F)': min_temp_fahrenheit,
        'Maximum Temperature (F)': max_temp_fahrenheit,
        'Pressure': pressure,
        'Humidity': humidity,
        'Wind Speed': wind_speed,
        'Time of Record': time_of_record,
        'Sunrise (Local Time)': sunrise_time,
        'Sunset (Local Time)': sunset_time
    }

    return transformed_weather_data

def write_weather_data(city_name, transformed_weather_data):
    #weather_data_df = pd.DataFrame(transformed_weather_data, index=[0])
    transformed_weather_data_list = [transformed_weather_data]
    weather_data_df = pd.DataFrame(transformed_weather_data_list)

    weather_data_file_path = '/Users/Shared/output/'
    weather_data_file_name = f"{city_name}_{dt.now().strftime('%Y%m%d%H%M%S')}_Weather_Data.csv"
    weather_data_df.to_csv(weather_data_file_path+weather_data_file_name, index=False)

def main():
    city_name = input("Enter a City Name: ").title()
    base_URL = "https://api.openweathermap.org/data/2.5/weather?q="

    with open('/Users/Shared/resource/openweathermap_apikey.txt', 'r') as read_apikey:
        apikey = read_apikey.read()

    full_URL = base_URL + city_name + "&appid=" + apikey

    request = requests.get(full_URL)
    response = request.json()
    weather_data = response

    transformed_weather_data = transform_weather_data(weather_data)
    write_weather_data(city_name, transformed_weather_data)

if __name__ == '__main__':
    main()
