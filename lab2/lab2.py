from flask import Flask, request, render_template
import pandas as pd
import numpy as np

app = Flask('__name__')

df = pd.read_csv("coffee.csv")

about = "Этот набор данных содержит информацию о ценах на кофе. Это даёт возможность для прогнозирования цен в будущем."
nulldf = "В данном наборе данных отсутсвуют нулевые значения!"
task1 = "Минимальная, максимальная, средняя цена открытия летом (во все года)"
task2 = "Минимальная, максимальная, средняя цена открытия зимой (по годам)"
task3 = "Минимальная, максимальная, средняя цена за выбранный год"
task4 = "Минимальная, максимальная, средняя цена открытия по годам"
task5 = "Зависимость кофе от объёма"



#начальная страница
@app.route('/')
def home():
    return render_template("home.html", about=about)

@app.route("/summer")
def summer_open():
    df['year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    summer = df.loc[(df['month'] >=6) & (df['month'] <= 8)].groupby('month').min()[['Open']]
    summer.rename(columns={'Open': 'Min Open'}, inplace=True)
    summer['Max Open'] = df.loc[(df['month'] >=6) & (df['month'] <= 8)].groupby('month').max()[['Open']]
    summer['Mean Open'] = df.loc[(df['month'] >=6) & (df['month'] <= 8)].groupby('month').mean()[['Open']].round(2)
    return task1 + summer.to_html(header="true", table_id="table")

@app.route("/winter")
def winter_open():
    df['year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    bf = df.loc[(df['month'] != 3) & (df['month'] != 4) & (df['month'] != 5) & (df['month'] != 6)
        & (df['month'] != 7) & (df['month'] != 7) & (df['month'] != 8) & (df['month'] != 9) & (df['month'] != 10) & (df['month'] != 11)]
    winter = bf.groupby(['year', 'month']).min()[['Open']]
    winter.rename(columns={'Open': 'Min Open'}, inplace=True)
    winter['Max Open'] = bf.groupby(['year', 'month']).max()[['Open']]
    winter['Mean Open'] = bf.groupby(['year', 'month']).mean()[['Open']].round(2)
    return task2 + winter.to_html(header="true", table_id="table")

@app.route("/year/", methods=['GET'])
def year_open():
    data = request.args;
    df['year'] = pd.DatetimeIndex(df['Date']).year
    select_year = df.loc[df['year'] == int(data['year'])].groupby('year').min()[['Open']]
    select_year.rename(columns={'Open': 'Min Open'}, inplace=True)
    select_year['Max Open'] = df.loc[df['year'] == int(data['year'])].groupby('year').max()[['Open']]
    select_year['Mean Open'] = df.loc[df['year'] == int(data['year'])].groupby('year').mean()[['Open']].round(2)
    return task3 + select_year.to_html(header="true", table_id="table")

@app.route("/years")
def years():
    df['year'] = pd.DatetimeIndex(df['Date']).year
    years = df.groupby('year').min()[['Open']]
    years.rename(columns={'Open': 'Min Open'}, inplace=True)
    years['Max Open'] = df.groupby('year').max()[['Open']]
    years['Mean Open'] = df.groupby('year').mean()[['Open']].round(2)
    return task4 + years.to_html(header="true", table_id="table")

@app.route("/volume")
def volume():
    coffee = df.groupby('Volume').min()[['Low']]
    coffee['High'] = df.groupby('Volume').max()[['High']]
    return task5 + coffee.to_html(header="true", table_id="table")



# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)