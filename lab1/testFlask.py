from flask import Flask, redirect, url_for_request
import requests

data_url = "https://www.kaggle.com/datasets/psycon/daily-coffee-price/download?datasetVersionNumber=32"
r = requests.get(data_url)
# r.headers

app = Flask(__name__)
@app.route("/")
def home():
    return "<html><form Action='http://127.0.0.1:5000/numtext' Method=get><input type=text size=20 name=name><input type=submit value='Кнопка'></html>"

@app.route("/")
def user(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    app.run(debug=True)