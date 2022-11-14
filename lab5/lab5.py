from flask import Flask, request, render_template, Response
import pandas as pd
import csv

app = Flask('__name__')

df = pd.read_csv("coffee.csv")

#read csv, and split on "," the line
csv_file = csv.reader(open('coffee.csv', "r"), delimiter=",")

kaggleArr = ["my", "Истюков Тимофей (12 вариант) — Цены на кофе",
             "https://www.kaggle.com/datasets/nancyalaswad90/yamana-gold-inc-stock-price", "Козлов Алексей (13 вариант) — Цены на акции",
             "https://www.kaggle.com/datasets/nancyalaswad90/diamonds-prices", "Долгов Кирилл (11 вариант) — Цены на бриллианты",
             "https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis", "Романова Аделина (21 вариант) — Данные о клиентах",
             "https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries", "Сергеев Евгений (24 вариант) — НЛО",
             "https://www.kaggle.com/datasets/surajjha101/stores-area-and-sales-data", "Дегтярёв Михаил (9 вариант) — Магазины",
             "https://www.kaggle.com/datasets/rashikrahmanpritom/heart-attack-analysis-prediction-dataset", "Фасхутдинов Идрис (2 вариант) — Сердечные приступы"
             ]

ArrKeyWord = ["coffee", "open", "close",
              "stock", "gold", "yamaha",
              "diamond", "carat", "clarity",
              "income", "education", "kidhome",
              "shape", "duration", "stats",
              "supermarket", "store", "sales",
              "age", "sex", "cp",
              ]

#начальная страница
@app.route('/')
def home():
    # return render_template("home.html", about=about)
    return render_template("home.html")


#справочник
@app.route('/linear_regression', methods=['GET'])
def linear_regression():
    lr_df = df['Close'].reset_index()   # цена закрытия
    lr_df.rename(columns={'Close': 'Y'}, inplace=True)
    lr_df['X'] = df['Volume']  # объём
    lr_df['XY'] = lr_df['X'] * lr_df['Y']
    lr_df['XX'] = lr_df['X'] * lr_df['X']
    sumY = lr_df['Y'].sum()
    sumX = lr_df['X'].sum()
    sumXY = lr_df['XY'].sum()
    sumXX = lr_df['XX'].sum()
    N = lr_df['index'].count()
    B1 = (sumXY-(sumY*sumX)/N) / (sumXX-sumX*sumX/N)
    B0 = (sumY-B1*sumX) / N

    data = request.args
    volume = data['volume']
    close = B1 * float(volume) + B0

    return render_template("linear_regression.html", volume=volume, close=close.round(2))

#справочник
@app.route('/more', methods=['GET'])
def more():
    lr_df = df['Close'].reset_index()   # цена закрытия
    lr_df.rename(columns={'Close': 'Y'}, inplace=True)
    lr_df['X'] = df['Volume']  # объём
    lr_df['XY'] = lr_df['X'] * lr_df['Y']
    lr_df['XX'] = lr_df['X'] * lr_df['X']
    sumY = lr_df['Y'].sum()
    sumX = lr_df['X'].sum()
    sumXY = lr_df['XY'].sum()
    sumXX = lr_df['XX'].sum()
    N = lr_df['index'].count()
    B1 = (sumXY-(sumY*sumX)/N) / (sumXX-sumX*sumX/N)
    B0 = (sumY-B1*sumX) / N
    return render_template("more.html", x="Объём", y="Цена закрытия", b0=B0, b1=B1) + lr_df.to_html()






# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)