import requests

# 2.0.1
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/", methods=["GET"])
def title_page():
    if 'city' in request.args:
        request_value, mess = request_openWeatherMap(request.args['city'])
    else:
        request_value, mess = request_openWeatherMap('Владимир')
        mess = "Вы ничего не ввели"
    return render_template( 
                        "index.html",
                        humidity=request_value['humidity'],
                        pressure=request_value['pressure'],
                        temperature=request_value['temperature'],
                        weather=request_value['weather'],
                        wind=request_value['wind'],
                        сity=request_value['сity'],
                        mess=mess)


def get_coordinates(city):
    list_coordinates = {
        'Владимир': {
            'lat': 56.08,
            'lon': 40.25
        },
        'Москва': {
            'lat': 55.75,
            'lon': 37.61
        },
        'Владивосток': {
            'lat': 44.07,
            'lon': 131.55
        }
    }
    if city in list_coordinates:
        return list_coordinates[city], None
    else:
        return list_coordinates['Владимир'], "Такого города ещё нет в БД"


def request_openWeatherMap(city):
    coordinat, mess = get_coordinates(city)
    url = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = 'afb43e8d675e4087555f08700c17393b'
    params = {
        'lat': coordinat['lat'],
        'lon': coordinat['lon'],
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru',
    }

    request_value = requests.get(url, params=params).json()
    # pprint.pprint(request)
    result = {
        'сity':           city,
        'temperature':    request_value['main']['temp'],
        'weather':        request_value['weather'][0]['description'],
        'wind':           request_value['wind']['speed'],
        'humidity':       request_value['main']['humidity'],
        'pressure':       request_value['main']['pressure']
    }
    return result, mess


if __name__ == '__main__':
    app.run(debug=True)
