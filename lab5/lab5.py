from flask import Flask, request, render_template, Response
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


#справочник
@app.route('/linear_regression', methods=['GET'])
def linear_regression():
    lr_df = df['Close'].reset_index()
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
    lr_df = df['Close'].reset_index()
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


@app.route('/lr_plot', methods=['GET'])
def lr_plot():
    lr_df = df['Close'].reset_index()
    lr_df.rename(columns={'Close': 'Y'}, inplace=True)
    lr_df['X'] = df['Volume']  # объём
    lr_df['XY'] = lr_df['X'] * lr_df['Y']
    lr_df['XX'] = lr_df['X'] * lr_df['X']
    sumY = lr_df['Y'].sum()
    sumX = lr_df['X'].sum()
    sumXY = lr_df['XY'].sum()
    sumXX = lr_df['XX'].sum()
    N = lr_df['index'].count()
    B1 = (sumXY - (sumY * sumX) / N) / (sumXX - sumX * sumX / N)
    B0 = (sumY - B1 * sumX) / N

    plt.scatter(df['Volume'].iloc[:round(N*0.99)], df['Close'].iloc[:round(N*0.99)], color='g')
    df['TestClose'] = B1 * df['Volume'] + B0
    plt.title('99% данных')
    plt.plot(df['Volume'].iloc[:round(N*0.99)], df['TestClose'].iloc[:round(N*0.99)], color='k')
    # plt.savefig('./plots/99proc.png')
    tmpfile = BytesIO() #создание временного файла
    plt.savefig(tmpfile, format='png')
    plt.clf()
    encoded1 = base64.b64encode(tmpfile.getvalue()).decode('utf-8') #кодирование

    plt.scatter(df['Volume'].iloc[round(N*0.99):], df['Close'].iloc[round(N*0.99):], color='g')
    df['TestClose'] = B1 * df['Volume'] + B0
    plt.title('оставшийся 1% данных')
    plt.plot(df['Volume'].iloc[round(N*0.99):], df['TestClose'].iloc[round(N*0.99):], color='k')
    #plt.savefig('./plots/1proc.png')
    tmpfile = BytesIO()  # создание временного файла
    plt.savefig(tmpfile, format='png')
    plt.clf()
    encoded2 = base64.b64encode(tmpfile.getvalue()).decode('utf-8')  # кодирование

    return render_template("lr_plot.html", encoded1=encoded1, encoded2=encoded2)


# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)