from flask import Flask, request, render_template, Response
from sklearn import tree
import pandas as pd
import csv
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask('__name__')

df = pd.read_csv("coffee.csv")

#read csv, and split on "," the line
csv_file = csv.reader(open('coffee.csv', "r"), delimiter=",")

#начальная страница
@app.route('/')
def home():
    # return render_template("home.html", about=about)
    return render_template("home.html")

@app.route('/test')
def test():
    return 'hello'



# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)