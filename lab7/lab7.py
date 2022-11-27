from flask import Flask, request, render_template, Response
import pandas as pd
import csv
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs
from clusterization import Clustering_KMeans
import seaborn as sns
from io import BytesIO
import base64

app = Flask('__name__')

df = pd.read_csv("coffee.csv")

#read csv, and split on "," the line
csv_file = csv.reader(open('coffee.csv', "r"), delimiter=",")

#начальная страница
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/plot_clustering', methods=['GET'])
def plot_clustering():
    data = request.args
    from_str = int(data['str_from'])
    to_str = int(data['str_to'])
    if from_str > to_str:
        from_str, to_str = to_str, from_str

    cluster_count = int(data['cluster_count'])
    encoded1 = before_clustering(from_str, to_str)
    encoded2 = after_clustering(from_str, to_str, cluster_count)
    return render_template("plot_clustering.html", encoded1=encoded1, encoded2=encoded2)


@app.route('/test2')
def after_clustering(from_str, to_str, cluster_count):

    centers = cluster_count
    X_train = df[['Close', 'Volume']].iloc[from_str:to_str].copy()
    X_train = StandardScaler().fit_transform(X_train)

    # поиск центроидов к набору данных
    kmeans = Clustering_KMeans(n_clusters=centers)
    kmeans.fit(X_train)

    # просмотр результатов
    class_centers, classification = kmeans.evaluate(X_train)
    sns.scatterplot(x=[X[0] for X in X_train],
                    y=[X[1] for X in X_train],
                    hue=classification,
                    style=classification,
                    palette="deep",
                    legend=None
                    )
    plt.plot([x for x, _ in kmeans.centroids],
             [y for _, y in kmeans.centroids],
             'k+',
             markersize=10,
             )
    plt.xlabel("Close")
    plt.ylabel("Volume")

    tmpfile = BytesIO()  # создание временного файла
    plt.title("После кластеризации")
    plt.savefig(tmpfile, format='png')
    plt.clf()
    plt.switch_backend('agg')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')  # кодирование
    tmpfile.close()

    return encoded

def before_clustering(from_str, to_str):
    plt.xlabel("Close")
    plt.ylabel("Volume")
    plt.scatter(df['Close'].iloc[from_str:to_str], df['Volume'].iloc[from_str:to_str], color='#76c2b4')

    tmpfile = BytesIO()  # создание временного файла
    plt.title("До кластеризации")
    plt.savefig(tmpfile, format='png')
    plt.clf()
    plt.switch_backend('agg')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')  # кодирование
    tmpfile.close()

    return encoded

@app.route('/dataframe')
def dataframe():
    return render_template("dataframe.html") + df[['Close', 'Volume']].to_html()


# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)