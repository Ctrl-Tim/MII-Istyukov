from flask import Flask, request, render_template
import matplotlib.pyplot as plt
import skfuzzy as fuzzy
from skfuzzy import control as ctrl
import numpy as np
from io import BytesIO
import base64

app = Flask('__name__')

#начальная страница
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/triangular')
def triangular():

    return render_template("triangular.html")

@app.route('/plot')
def triplot():
    encoded = triangular_plot()
    return render_template("trimf.html", encoded=encoded)

@app.route('/trimf', methods=['GET'])
def triangular_plot():
    data = request.args
    student = ctrl.Antecedent(np.arange(0, 200, 1), 'student')
    for i in range(int(data['count'])):
        name = 'record' + str(i)
        min_name = 'min' + str(i)
        mode_name = 'mode' + str(i)
        max_name = 'max' + str(i)
        student[data[name]] = fuzzy.trimf(student.universe, [int(data[min_name]), int(data[mode_name]), int(data[max_name])])

    # график
    tmpfile = BytesIO()  # создание временного файла
    student.view()
    plt.title("Судьба на ФИСТе")
    plt.xlabel("Кол-во клиентов в месяц")
    plt.ylabel("Степень принадлежности")
    plt.savefig(tmpfile, format='png')
    plt.clf()
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')  # кодирование
    tmpfile.close()
    return encoded



# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)