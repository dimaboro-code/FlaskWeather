import datetime
from flask import Flask, render_template
import requests


appid = "19cb7aa1bae799b795198910a7b33414"
value2 = []


def get_wind_direction(deg):
    windrose = ['С ', 'СВ', ' В', 'ЮВ', 'Ю ', 'ЮЗ', ' З', 'СЗ']
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
        pass
    assert isinstance(city_id, int)
    return city_id


def request_forecast(city_id):
    global value2
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        temp = ('город:', data['city']['name'], data['city']['country'])
        value1 = ' '.join(temp)
        for i in data['list']:
            temp = ((i['dt_txt'])[:16], '{0:+3.0f}'.format(i['main']['temp']),
                    '{0:2.0f}'.format(i['wind']['speed']) + " м/с",
                    get_wind_direction(i['wind']['deg']),
                    i['weather'][0]['description'])
            temp2 = " ".join(temp)
            [value2.append(temp2) if int(temp2[9]) == int(str(datetime.date.today())[9]) + 1 else None]
        print(value2)
        return value1, value2
    except Exception as e:
        print("Exception (forecast):", e)
        pass


city_id = get_city_id('Moscow, Ru')
value1, value2 = request_forecast(city_id)
app = Flask(__name__)


@app.route('/')
def page():
    return render_template('page.html', value1=value1, value2=value2)


if __name__ == "__main__":
    app.run()
