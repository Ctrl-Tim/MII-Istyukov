from flask import Flask, request, render_template, Response
import pandas as pd
from datetime import datetime, timedelta
import sys
from bloomfilter import BloomFilter
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
@app.route('/bloom_filter', methods=['GET'])
def search():
    data = request.args
    bloom_filter = BloomFilter(200, 100)

    for i in range(len(ArrKeyWord)):
        bloom_filter.add_to_filter(ArrKeyWord[i])

    if not bloom_filter.check_is_not_in_filter(data['keyWord']):
        for i in range(len(ArrKeyWord)):
            if ArrKeyWord[i] == data['keyWord']:
                place = i
                break

        if place // 3 == 0:
            newdf = df.iloc[0: 100]
            return render_template('result_my_lab.html') + newdf.to_html()

        else:
            return render_template("result_other.html", kaggle_link=kaggleArr[(place//3)*2], student_info=kaggleArr[(place//3)*2+1])

    else:
        return render_template("notfound.html")





# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)