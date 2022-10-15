from flask import Flask, request, render_template, Response
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io
import json
import plotly
import plotly.express as px

app = Flask('__name__')

df = pd.read_csv("coffee.csv")

about = "Этот набор данных содержит информацию о ценах на кофе. Это даёт возможность для прогнозирования цен в будущем."
nulldf = "В данном наборе данных отсутсвуют нулевые значения!"

task1 = "Минимальная, максимальная, средняя цена открытия летом (во все года)"
task2 = "Минимальная, максимальная, средняя цена открытия зимой (по годам)"
task3 = "Минимальная, максимальная, средняя цена за выбранный год"
task4 = "Минимальная, максимальная, средняя цена открытия по годам"



#начальная страница
@app.route('/')
def home():
    return render_template("home.html", about=about)

@app.route('/summer_plot')
def summer_plot():
    df['year'] = pd.DatetimeIndex(df['Date']).year
    summer = df.groupby('year').min()[['Open']].reset_index()
    summer.rename(columns={'Open': 'Min Open'}, inplace=True)
    summer['Max Open'] = df.groupby('year').max()[['Open']].reset_index(drop=True)
    summer['Mean Open'] = df.groupby('year').mean()[['Open']].reset_index(drop=True)

    fig = px.bar(summer, x='year', y=["Min Open", "Mean Open", "Max Open"])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphJSON=graphJSON, description=task1)

@app.route('/winter_plot')
def winter_plot():
    df['year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    bf = df.loc[(df['month'] != 3) & (df['month'] != 4) & (df['month'] != 5) & (df['month'] != 6)
                & (df['month'] != 7) & (df['month'] != 7) & (df['month'] != 8) & (df['month'] != 9) & (
                            df['month'] != 10) & (df['month'] != 11)]
    winter = bf.groupby(['year', 'month']).min()[['Open']]
    winter.rename(columns={'Open': 'Min Open'}, inplace=True)
    winter['Max Open'] = bf.groupby(['year', 'month']).max()[['Open']]
    winter['Mean Open'] = bf.groupby(['year', 'month']).mean()[['Open']].round(2)

    fig = px.bar(winter, x='year', y='Min Open', color='month', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphJSON=graphJSON, description=task2)

@app.route('/years_plot')
def years_plot():
    df['year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    fig = px.bar(df, x='year', y='Open', color='month', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphJSON=graphJSON, description=task4)

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    x = df.head().Date
    y = df.head().Open

    ax.bar(x, y, color = "#304C89")

    plt.xticks(rotation = 30, size = 5)
    plt.ylabel("Expected Clean Sheets", size = 5)

    return fig



# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)