from flask import Flask, request, render_template
import matplotlib.pyplot as plt
import skfuzzy as fuzzy
from skfuzzy import control as ctrl
import numpy as np
from io import BytesIO
import base64

app = Flask('__name__')

# линг.переменная (min, mode, max, степень принадлежности)
dict = {"Программист": (0, 0, 30, -1), "Ради корочки": (25, 50, 70, -1), "Отчисленный": (60, 150, 150, -1)}

#начальная страница
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/trimf', methods=['GET'])
def trimf():
    data = request.args
    hours = int(data['hours'])

    for key in dict:
        values = dict.get(key)
        min = values[0]
        mode = values[1]
        max = values[2]

        if min <= hours <= mode:
            mf = 1 - ((mode - hours) / (mode - min))
        elif mode <= hours <= max:
            mf = 1 - ((hours - mode) / (max - mode))
        else:
            mf = 0
        new_val = (min, mode, max, mf)
        dict.update({key: new_val})

    mf_min = dict.get("Программист")[3]
    mf_mode = dict.get("Ради корочки")[3]
    mf_max = dict.get("Отчисленный")[3]

    result = ""
    mf = -1

    if hours > max or hours < min:
        result = "Ошибка"
    elif mf_max <= mf_min >= mf_mode:
        result = "Программист"
        mf = round(mf_min, 2)
    elif mf_max <= mf_mode >= mf_min:
        result = "Ради корочки"
        mf = round(mf_mode, 2)
    elif mf_min <= mf_max >= mf_mode:
        result = "Отчисленный"
        mf = round(mf_max, 2)

    encoded = plot_fuzzy(hours, mf)

    return render_template("trimf.html", hours=hours, encoded=encoded, result=result, mf=mf)


def plot_fuzzy(hours, mf):
    student = ctrl.Antecedent(np.arange(0, 160, 1), 'student')
    for key in dict:
        values = dict.get(key)
        if (key == "Программист"):
            student['Программист'] = fuzzy.trimf(student.universe, [values[0], values[1], values[2]])
        elif (key == "Ради корочки"):
            student['Ради корочки'] = fuzzy.trimf(student.universe, [values[0], values[1], values[2]])
        elif (key == "Отчисленный"):
            student['Отчисленный'] = fuzzy.trimf(student.universe, [values[0], values[1], values[2]])
    # график
    tmpfile = BytesIO()  # создание временного файла
    student.view()
    plt.title("Судьба на ФИСТе")
    plt.xlabel("Часы")
    plt.ylabel("Степень принадлежности")
    plt.scatter(hours, mf, color='red', s=40, marker='o')
    plt.savefig(tmpfile, format='png')
    plt.clf()
    plt.switch_backend('agg')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')  # кодирование
    tmpfile.close()
    return encoded

# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)