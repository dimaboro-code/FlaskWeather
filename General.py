from flask import Flask, render_template
import owm_request


app = Flask(__name__)


@app.route('/')
def page():
    return render_template('page.html', value=owm_request.request_forecast(owm_request.city_id))

if __name__ == "__main__":
    app.run()
