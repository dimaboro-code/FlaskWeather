import datetime
from flask import Flask, render_template
import requests


appid = "19cb7aa1bae799b795198910a7b33414"


def get_wind_direction(deg):
    windrose = ['Север ', 'СевероВосток', ' Восток', 'ЮгоВосток', 'Юг ', 'ЮгоЗапад', ' Запад', 'СевероЗапад']
    for i in range(0, 8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = windrose[i]
            break
    return res


def get_city_id(s_city_name):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city_name, 'type': 'like', 'units': 'metric',
                                   'lang': 'ru', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:
        print("Exception (find):", e)
    assert isinstance(city_id, int)
    return city_id


def request_forecast(city_id):
    weather_of_day = []
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        place = ' '.join(('город:', data['city']['name'], data['city']['country']))
        for forecast in data['list']:
            forecast_string = " ".join(((forecast['dt_txt'])[:16], '{0:+3.0f}'.format(forecast['main']['temp']),
                            '{0:2.0f}'.format(forecast['wind']['speed']) + " м/с",
                            get_wind_direction(forecast['wind']['deg']),
                            forecast['weather'][0]['description']))
            [weather_of_day.append(forecast_string) if int(forecast_string[9])
                                                        == int(str(datetime.date.today())[9]) + 1 else None]
        return place, weather_of_day
    except Exception as e:
        print("Exception (forecast):", e)


app = Flask(__name__)


@app.route('/')
def page():
    city_id = get_city_id('Moscow, Ru')
    place, weather_of_day = request_forecast(city_id)
    return render_template('page.html', place=place, weather_of_day=weather_of_day)


if __name__ == "__main__":
    app.run()
