from flask import Flask, request, render_template, Response
import pandas as pd
from datetime import datetime, timedelta
import json
import plotly
import plotly.express as px

app = Flask('__name__')

df = pd.read_csv("coffee.csv")

about = "Этот набор данных содержит информацию о ценах на кофе. Это даёт возможность для прогнозирования цен в будущем. "
nulldf = "В данном наборе данных отсутсвуют нулевые значения!"
approximate = "Используемые данные (с приблизительными значениями на последующие года). "

task1 = "Минимальная, максимальная, средняя цена открытия летом (во все года)"
task2 = "Минимальная, максимальная, средняя цена открытия зимой (по годам)"
task3 = "Минимальная, максимальная, средняя цена за выбранный год"
task4 = "Минимальная, максимальная, средняя цена открытия по годам"

dates = pd.date_range(df.iloc[df['Date'].count()-1]['Date'], periods=(int)(df['Date'].count()*0.1))

#дополнение данных приблизительными значениями
for i in range(df.shape[0]-1, round(df.shape[0]*1.1), 1):
    date = datetime.strptime(df['Date'].values[i], "%Y-%m-%d")
    next_date = datetime.strftime(date + timedelta(days=1), "%Y-%m-%d") #следующий день
    next_open = df['Open'].value_counts().rename_axis('Open').to_frame('counts').index[i%50]
    next_high = df['High'].value_counts().rename_axis('High').to_frame('counts').index[i % 50]
    next_low = df['Low'].value_counts().rename_axis('Low').to_frame('counts').index[i % 50]
    next_close = df['Low'].value_counts().rename_axis('Low').to_frame('counts').index[i % 50]
    next_low = df['Close'].value_counts().rename_axis('Close').to_frame('counts').index[i % 50]
    next_volume = df['Volume'].value_counts().rename_axis('Volume').to_frame('counts').index[i % 50]
    next_currency = 'USD'

    new_row = [next_date, next_open, next_high, next_low, next_close, next_volume, next_currency]
    df.loc[i+1] = new_row

#начальная страница
@app.route('/')
def home():
    return render_template("home.html", about=about)


#справочник
@app.route('/df_info')
def df_info():
    return approximate + about + nulldf + df.to_html()

@app.route('/summer_plot')
def summer_plot():
    # df['year'] = pd.DatetimeIndex(df['Date']).year
    # summer = df.groupby('year').min()[['Open']].reset_index()
    # summer.rename(columns={'Open': 'Min Open'}, inplace=True)
    # summer['Max Open'] = df.groupby('year').max()[['Open']].reset_index(drop=True)
    # summer['Mean Open'] = df.groupby('year').mean()[['Open']].reset_index(drop=True)

    df['year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    summer = df.loc[(df['month'] >= 6) & (df['month'] <= 8)].groupby('month').min()[['Open']].reset_index()
    summer.rename(columns={'Open': 'Min Open'}, inplace=True)
    summer['Max Open'] = df.loc[(df['month'] >= 6) & (df['month'] <= 8)].groupby('month').max()[['Open']].reset_index(drop=True)
    summer['Mean Open'] = df.loc[(df['month'] >= 6) & (df['month'] <= 8)].groupby('month').mean()[['Open']].round(2).reset_index(drop=True)


    fig = px.bar(summer, x='month', y=["Min Open", "Mean Open", "Max Open"])
    fig.update_layout(legend=dict(font=dict(size=16)))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphJSON=graphJSON, description=task1)

@app.route('/winter_plot')
def winter_plot():
    df['year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    bf = df.loc[(df['month'] != 3) & (df['month'] != 4) & (df['month'] != 5) & (df['month'] != 6)
                & (df['month'] != 7) & (df['month'] != 7) & (df['month'] != 8) & (df['month'] != 9) & (
                            df['month'] != 10) & (df['month'] != 11)]
    winter = bf.groupby(['year', 'month']).min()[['Open']].reset_index()
    winter.rename(columns={'Open': 'Min Open'}, inplace=True)
    winter['Max Open'] = bf.groupby(['year', 'month']).max()[['Open']].reset_index(drop=True)
    winter['Mean Open'] = bf.groupby(['year', 'month']).mean()[['Open']].round(2).reset_index(drop=True)

    fig = px.bar(winter, x='year', y=["Min Open", "Mean Open", "Max Open"], color='month')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphJSON=graphJSON, description=task2)

@app.route('/years_plot')
def years_plot():
    df['year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    fig = px.bar(df, x='year', y='Open', color='month', barmode='group')
    # fig = px.scatter(df, x='year', y='Open', color='month')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphJSON=graphJSON, description=task4)


@app.route("/year/", methods=['GET'])
def year_open():
    data = request.args;
    df['year'] = pd.DatetimeIndex(df['Date']).year
    select_year = df.loc[df['year'] == int(data['year'])].groupby('year').min()[['Open']]
    select_year.rename(columns={'Open': 'Min Open'}, inplace=True)
    select_year['Max Open'] = df.loc[df['year'] == int(data['year'])].groupby('year').max()[['Open']]
    select_year['Mean Open'] = df.loc[df['year'] == int(data['year'])].groupby('year').mean()[['Open']].round(2)
    return task3 + select_year.to_html(header="true", table_id="table")

# @app.route('/plot.png')
# def plot_png():
#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')
#
# def create_figure():
#     fig, ax = plt.subplots(figsize = (6,4))
#     fig.patch.set_facecolor('#E8E5DA')
#
#     x = df.head().Date
#     y = df.head().Open
#
#     ax.bar(x, y, color = "#304C89")
#
#     plt.xticks(rotation = 30, size = 5)
#     plt.ylabel("Expected Clean Sheets", size = 5)
#
#     return fig



# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)