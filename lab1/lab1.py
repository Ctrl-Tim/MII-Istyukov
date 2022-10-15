from flask import Flask, request, render_template
import pandas as pd

app = Flask('__name__')

#начальная страница
@app.route('/')
def home():
    return render_template("home.html")

#чтение данных csv-файла
@app.route('/diapason', methods=['GET'])
def diapason():
    data = request.args
    df = pd.read_csv('coffee1.csv', sep=',')

    # Проверяем диапазон строк
    if int(data['from']) > int(data['to']):
        from_str = int(data['to'])
        to_str = int(data['from'])
    else:
        from_str = int(data['from'])
        to_str = int(data['to'])

    # Проверяем диапазон стобцов
    if int(data['from_st']) > int(data['to_st']):
        from_stl = int(data['to_st'])
        to_stl = int(data['from_st'])
    else:
        from_stl = int(data['from_st'])
        to_stl = int(data['to_st'])

    prim = df.iloc[from_str: to_str, from_stl: to_stl]

    count = df.isna().sum()
    countAll = df.count()

    description_date1 = 'Описание: набор данных предназначен для прогнозирования цены на кофе. ' \
                        'Удобно для регулярного анализа настроений рынка и прогнозирования ценовых изменений в будущем на основе выявленных паттернов.' \
                        'Также это поможет отличить «бычий» рынок (цена закрытия выше, чем цена открытия) от «медвежьего» (цена закрытия ниже, чем цена открытия).'
    description_date2 = 'Описание стоблцов таблицы:'
    description_date3 = str(df.dtypes)

    return render_template("diapason.html", count=count, countAll=countAll, len_str=len(df.axes[0]), len_stl=len(df.axes[1]),
                           description_date1=description_date1, description_date2=description_date2, description_date3=description_date3) \
                            + "<div align='center' class='table table-bordered'>" + prim.to_html() + "</div>" \
                            + "*показывает объем для определенного ценового диапазона, который основан на ценах закрытия"
    # return '<h1 align="center">Набор данных для прогнозирования цен на кофе</h1><br>' \
    #         + '<div align="center">' + prim.to_html() + '</div>'\
    #         + '<br><h3>Количество пустых ячеек = %s , ' % count \
    #         + '<br>Количество заполненных ячеек = %s , ' % countAll \
    #         + '<br>Количество строк = %s , ' % len(df.axes[0]) \
    #         + '<br>Количество столбцов = %s</h3>' % len(df.axes[1]) + '<h4>%s</h4>' %description_date

# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)