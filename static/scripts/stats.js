function FiltersRender(operations, categories){
    /*
    Функция для обработки фильтров и построения круговых диаграмм
    - operations: операции пользователя
    - categories: категории пользователя
     */
    try{
        document.getElementById('minus_diagram').innerHTML = "";
        document.getElementById('plus_diagram').innerHTML = "";

        let filtered_categories = [];

        let cats_filter = document.getElementsByClassName("categorie_checkbox");
        for(let cat of cats_filter) {
            if (cat.checked && cat.name.includes("categorie")) {
                filtered_categories.push(Number(cat.name.split('_')[1]));
            }
        }
        let date_start = null;
        if(document.getElementById("date_start").value) {
            date_start = new Date(
                    document.getElementById("date_start").value.toString() + " UTC+3"
            )
        }
        else{
            date_start = new Date(1970, 1, 1, 0, 0, 0);
        }


        let date_end = null;
        if(document.getElementById("date_end").value){
            date_end = new Date(
                    document.getElementById("date_end").value.toString() + " UTC+3"
            )
            date_end.setDate(date_end.getDate() + 1);
            date_end.setSeconds(date_end.getSeconds() - 1);
        }
        else{
            date_end = new Date(2100, 12, 31, 23, 59, 59);
        }

        let filters = {
            categories: filtered_categories,
            dates: [date_start, date_end]
        }


        let minus_data = {}
        let plus_data = {}
        for(let ctg of filtered_categories){
            minus_data[ctg] = 0;
            plus_data[ctg] = 0;
        }
        for(op of operations){
            let op_date = new Date(Date.parse(op[3]))

            // console.log(op[1] === 0, filtered_categories.includes(op[2]),
            //     op_date >= date_start, op_date <= date_end)

            if (op[1] === 0 && filtered_categories.includes(op[2]) &&
                op_date >= date_start && op_date <= date_end){
                minus_data[op[2]] += op[4];
            }
            else if(op[1] === 1 && filtered_categories.includes(op[2]) &&
                op_date >= date_start && op_date <= date_end){
                plus_data[op[2]] += op[4];
            }
        }
        // console.log(minus_data)
        let minus_pie_data = []
        let plus_pie_data = []
        let minus_amount = 0;
        let plus_amount = 0;
        for(let ctg in minus_data) {
            let category = category_by_id(categories, ctg)
            if (category) {
                //console.log(category)
                minus_amount += minus_data[ctg]
                minus_pie_data.push({
                    x: category[2],
                    value: minus_data[ctg],
                    normal: {fill: category[1]},
                    legendItem: {
                        enabled: !(minus_data[ctg] === 0)
                    }
                })
            }
        }
        for(let ctg in plus_data) {
            let category = category_by_id(categories, ctg)
            if (category) {
                //console.log(category)
                plus_amount += plus_data[ctg]
                plus_pie_data.push({
                x: category[2],
                value: plus_data[ctg],
                normal: {fill: category[1]},
                legendItem: {
                    enabled: !(plus_data[ctg] === 0)
                }
                })

            }
        }
        // create a chart and set the data

        document.getElementById("minus_diagram").style.height =
            document.getElementById("fixed_container").offsetHeight;

        document.getElementById("plus_diagram").style.height =
            document.getElementById("fixed_container").offsetHeight;

        var minus_chart = anychart.pie();

        minus_chart.data(minus_pie_data)
        minus_chart.title(`Расходы\n${minus_amount} руб.`)
        // set the container id
        minus_chart.container("minus_diagram");

        // initiate drawing the minus_chart


        var plus_chart = anychart.pie();

        plus_chart.data(plus_pie_data)
        plus_chart.title(`Доходы\n${plus_amount} руб.`)
        // set the container id
        plus_chart.container("plus_diagram");

        // initiate drawing the plus_chart

        minus_chart.labels().format('{%X}')
        plus_chart.labels().format('{%X}')

        minus_chart.tooltip().format('{%value} руб.')
        plus_chart.tooltip().format('{%value} руб.')

        minus_chart.draw();
        plus_chart.draw();

    }
    catch (e) {
        console.log(e);
    }

}

function category_by_id(categories, id) {
    /*
    Функция для получения категории по идентификатору
    categories: массив категорий
    id: идентификатор
     */
    for(let ctg of categories){
        // console.log(ctg[0], id);
        if(ctg[0] === Number(id)){
            return ctg;
        }
    }
    return null;
}


function exportStats(format) {
    /*
    Функция для обработки фильтров даты и экспорта данных
    - format: формат, в котором пользователь хочет скачать файл
     */
    let date_start = null;
    if(document.getElementById("date_start").value) {
        date_start = new Date(
                document.getElementById("date_start").value.toString() + " UTC+3"
        )
    }
    else{
        date_start = new Date(1970, 1, 1, 0, 0, 0);
    }


    let date_end = null;
    if(document.getElementById("date_end").value){
        date_end = new Date(
                document.getElementById("date_end").value.toString() + " UTC+3"
        )
        date_end.setDate(date_end.getDate() + 1);
        date_end.setSeconds(date_end.getSeconds() - 1);
    }
    else{
        date_end = new Date(2100, 12, 31, 23, 59, 59);
    }
    date_start = date_start.toISOString().split('T')[0]
    date_end = date_end.toISOString().split('T')[0]

    let url = `/download_statistic/from=${date_start}&to=${date_end}&format=${format}`
    window.open(url, '_blank')
}


function linereg_diagram(operations) {
    /*
    Функция для построения графика линейной регрессии
    и подсчета прогноза расходов на текущий месяц
    - operations: операции пользователя
     */
    let start_date = (new Date())
    start_date.setDate(0)
    let end_date = new Date();
    end_date.setMonth(end_date.getMonth() + 1)
    end_date.setDate(0);

    let amounts = [];
    amounts.length = end_date.getDate() + 1
    amounts.fill(0);

    for(let op of operations){
        let op_date = new Date(Date.parse(op[3]))
        let dif1 = Math.floor((op_date.getTime() - start_date.getTime()) / (3600 * 24 * 1000));
        let dif2 = Math.floor((end_date.getTime() - op_date.getTime()) / (3600 * 24 * 1000));
        if (dif1 >= 0 && dif2 >= 0 && op[1] === 0){
            console.log(dif1);
            amounts[dif1] += op[4];
        }
    }

    let rawData = []
    for(let i = 0; i < amounts.length; i++){
        if(amounts[i] > 0 && rawData.length > 0){
            rawData.push([i + 1, amounts[i] + rawData[rawData.length-1][1]])
        }
        else if(amounts[i] > 0){
            rawData.push([i + 1, amounts[i]])
        }
    }
    let result = regression('linear', rawData);
    let coeff = result.equation;

    let data_1 = rawData;
    console.log(amounts)
    let data_2 = setTheoryData(rawData, coeff, amounts.length);

    chart = anychart.scatter();

    let series1 = chart.marker(data_1);
    series1.name("Точное значение");

    let series2 = chart.line(data_2);
    series2.name("Прогноз");
    series2.markers(true);

    series1.tooltip().format("День месяца: {%X}\nПотрачено: {%value}{decimalsCount:2} руб.")
    series2.tooltip().format("День месяца: {%X}\nПотрачено: {%value}{decimalsCount:2} руб.")

    document.getElementById("forecast").innerHTML = `
        Прогноз общих расходов к концу месяца:
        <span class="forecast_number">${formula(coeff, amounts.length - 1).toFixed(2)}</span>
        руб.
    `

    chart.container("linereg_diagram");
    chart.draw();

}

function formula(coeff, x) {
    /*
    Функция для подсчета значения линейной регрессии
    на координате x
    - coeff: данные функции регрессии
    - x: аргумент x

    Возвращает значение функции линейной регрессии
     */
    let result = null;
    for (let i = 0, j = coeff.length - 1; i < coeff.length; i++, j--) {
        result += coeff[i] * Math.pow(x, j);
    }
    return result;
}

function setTheoryData(rawData, coeff, len) {
    /*
    Функция для подсчета прогнозов трат на каждый день
    текущего месяца
    - rawData: информация о расходах в этом месяце
    - coeff: данные функции регрессии
    - len: длина текущего месяца в днях

    Возвращает массив прогнозов (теоретически высчитанных расходов)
     */
  let theoryData = [];
  try{
      for (let i = rawData[0][0]; i < len; i++) {
          theoryData[i] = [i, formula(coeff, i)];
      }
  }
  finally{
    return theoryData;
  }
}


let CPIs = {
    "2021-1": 5.19,
    "2021-2": 5.67,
    "2021-3": 5.78,
    "2021-4": 5.52,
    "2021-5": 6.01,
    "2021-6": 6.51,
    "2021-7": 6.47,
    "2021-8": 6.69,
    "2021-9": 7.41,
    "2021-10": 8.14,
    "2021-11": 8.40,
    "2021-12": 8.39,
    "2022-1": 8.74,
    "2022-2":9.2,
    "2022-3":16.7
}

function calculate_inflation(monthes, amount) {
    /*
    Функция для пересчета суммы относительно инфляции
    - monthes: количество месяцев
    - amount: сумма
     */
    let FV = amount;
    let t = monthes / 12
    let new_date = new Date()
    new_date.setMonth(new_date.getMonth() - monthes - 1)


    let r = CPIs[`${new_date.getFullYear()}-${new_date.getMonth() + 1}`] / 100

    let result = (FV / Math.pow((1 + r), t)).toFixed(2)
    // return parse_amount(result)
    document.getElementById(`inf-${monthes}`)
        .getElementsByClassName('inf_balance_amount_big')[0]
        .innerHTML = parse_amount(result)[0]
    document.getElementById(`inf-${monthes}`)
        .getElementsByClassName('inf_balance_amount_small')[0]
        .innerHTML = "," + parse_amount(result)[1]
}

function parse_amount(amount) {
    /*
    Функция для разбиения десятичной дроби на
    целую и дробную часть
    - amount: число
     */
    return String(amount).split('.')
}