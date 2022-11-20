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

@app.route('/predict',  methods=['GET'])
def predict():
    df['Year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    df['Season'] = '?'
    df.loc[((df['month'] == 12) | (df['month'] == 1) | (df['month'] == 2)), 'Season'] = 'winter'
    df.loc[((df['month'] >= 3) & (df['month'] <= 5)), 'Season'] = 'spring'
    df.loc[((df['month'] >= 6) & (df['month'] <= 8)), 'Season'] = 'summer'
    df.loc[((df['month'] >= 9) & (df['month'] <= 11)), 'Season'] = 'autumn'
    df_seasons = df.groupby(['Year', 'Season']).min()[['Open']].reset_index()

    X = df_seasons['Open'].reset_index().iloc[0:30, 1:]
    Y = df_seasons['Season'].reset_index().iloc[:30, 1:2]
    model = tree.DecisionTreeClassifier(criterion="entropy")
    model.fit(X, Y)

    data = request.args
    open = data['open']
    predict_season = str(model.predict([[float(open)]]))

    return render_template("predict.html", open=open, predict_season=predict_season)

@app.route('/tree_season')
def tree_season():
    df['Year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    df['Season'] = '?'
    df.loc[((df['month'] == 12) | (df['month'] == 1) | (df['month'] == 2)), 'Season'] = 'winter'
    df.loc[((df['month'] >= 3) & (df['month'] <= 5)), 'Season'] = 'spring'
    df.loc[((df['month'] >= 6) & (df['month'] <= 8)), 'Season'] = 'summer'
    df.loc[((df['month'] >= 9) & (df['month'] <= 11)), 'Season'] = 'autumn'
    df_seasons = df.groupby(['Year', 'Season']).min()[['Open']].reset_index()

    X = df_seasons['Open'].reset_index().iloc[0:30, 1:]
    Y = df_seasons['Season'].reset_index().iloc[:30, 1:2]
    model = tree.DecisionTreeClassifier(criterion="entropy")
    model.fit(X, Y)
    plt.figure(figsize=(20,20))
    tree.plot_tree(model)

    tmpfile = BytesIO()  # создание временного файла
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')  # кодирование

    return render_template("tree.html", encoded=encoded, score=model.score(X,Y).round(2))

@app.route('/seasons_of_years')
def seasons_of_years():
    df['year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    df['season'] = '?'
    df.loc[((df['month'] == 12) | (df['month'] == 1) | (df['month'] == 2)), 'season'] = 'winter'
    df.loc[((df['month'] >= 3) & (df['month'] <= 5)), 'season'] = 'spring'
    df.loc[((df['month'] >= 6) & (df['month'] <= 8)), 'season'] = 'summer'
    df.loc[((df['month'] >= 9) & (df['month'] <= 11)), 'season'] = 'autumn'
    df_seasons = df.groupby(['year', 'season']).min()[['Open']]
    return render_template("seasons_of_years.html") + df_seasons.to_html()

@app.route('/model_evaluation')
def model_evaluation():
    df['Year'] = pd.DatetimeIndex(df['Date']).year
    df['month'] = pd.DatetimeIndex(df['Date']).month
    df['Season'] = '?'
    df.loc[((df['month'] == 12) | (df['month'] == 1) | (df['month'] == 2)), 'Season'] = 'winter'
    df.loc[((df['month'] >= 3) & (df['month'] <= 5)), 'Season'] = 'spring'
    df.loc[((df['month'] >= 6) & (df['month'] <= 8)), 'Season'] = 'summer'
    df.loc[((df['month'] >= 9) & (df['month'] <= 11)), 'Season'] = 'autumn'
    df_seasons = df.groupby(['Year', 'Season']).min()[['Open']].reset_index()

    X = df_seasons['Open'].reset_index().iloc[0:30, 1:]
    Y = df_seasons['Season'].reset_index().iloc[:30, 1:2]
    model = tree.DecisionTreeClassifier(criterion="entropy")
    model.fit(X, Y)

    XY_real = df_seasons['Open'].reset_index().iloc[30:40, 1:]
    XY_real['Season'] = df_seasons['Season'].reset_index().iloc[30:40, 1:2]
    XY_train = XY_real.copy()
    # XY_train['Season'] = str(model.predict([[float(XY_train['Open'])]]))
    XY_train['Season'] = XY_train['Open'].apply(lambda x: model.predict([[float(x)]]))

    evaluation = XY_real.copy()
    evaluation['Season train'] = XY_train['Season']
    evaluation.loc[(evaluation['Season'] == evaluation['Season train']), 'equals'] = 'True'
    evaluation.loc[(evaluation['Season'] != evaluation['Season train']), 'equals'] = 'False'
    result = evaluation['equals'].loc[evaluation['equals'] == 'True'].count() / evaluation['equals'].count()


    return render_template("model_evaluation.html", result=result*100) \
           + '<br>Реальные данные' + XY_real.to_html() + '<br>Сгенерированные данные' + XY_train.to_html()



# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)