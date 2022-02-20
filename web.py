from config import *
from engine import *

@app.route('/')
def main_page():
    session['last_page'] = '/'
    return render_template('main.html')

@app.route('/login', methods=["GET"])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def login_POST():
    user = user_by_email(request.form['email'])
    if not user:
        return render_template('login.html', error=1)
    else:
        if user.password == request.form['password']:
            session['user_id'] = user.id
        else:
            return render_template('login.html', error=1)

    if 'last_page' in session:
        return redirect(session['last_page'])
    return redirect('/')

@app.route('/reg', methods=["GET"])
def reg_page():
    return render_template('reg.html')

@app.route('/reg', methods=["POST"])
def reg_POST():
    user = user_by_email(request.form['email'])
    if user:
        return render_template('reg.html', error=1)
    else:
        if request.form['password1'] == request.form['password2']:
            user = User(
                id=-1,
                email=request.form['email'],
                password=request.form['password1'],
                name=request.form['name'],
                balance=0
            )
        else:
            return render_template('reg.html', error=1)

    if 'last_page' in session:
        return redirect(session['last_page'])
    return redirect('/')


@app.route('/operations', methods=['GET'])
def operations_page():
    try:
        session['last_page'] = '/operations'
        if "user_id" not in session:
            return redirect('/login')

        user = user_by_id(int(session['user_id']))
        balance = parse_amount(user.balance)
        last_op_id = 0
        if len(operations) > 0:
            last_op_id = operations[-1].id + 1
        rows = [[], [], last_op_id, balance]

        for ctg in categories:
            ctg: Category
            if ctg.user.id == user.id:
                rows[0].append([
                    ctg.id,
                    ctg.color,
                    ctg.name
                ])

        for op in operations:
            op: Operation
            if op.user.id == user.id:
                date = render_date(op.date)
                key = -1
                for d in range(len(rows[1])):
                    if rows[1][d][0] == date:
                        key = d
                        break
                if key == -1:
                    rows[1].append([date,[]])

                amount_big, amount_small = parse_amount(op.amount)

                rows[1][key][1].append(
                    [
                        op.category.id,
                        str(op.date),
                        op.type,
                        amount_big,
                        amount_small,
                        op.description,
                        op.category.color,
                        op.id,
                        op.category.name
                    ]
                )
        rows[1] = sorted(rows[1], key=lambda i: unrender_date(i[0]), reverse=True)

        return render_template('operations.html', rows=rows)

    except Exception as e:
        print(e)
        return redirect('/')


@app.route('/operations', methods=['POST'])
def operations_POST():
    try:
        session['last_page'] = '/operations'
        if "user_id" not in session:
            return redirect('/login')

        user = user_by_id(int(session['user_id']))
        new_category = int(request.form.get('popup_ctg'))
        new_description = request.form.get('popup_description_text').replace('<br>','\n')
        new_date = request.form.get('popup_date').replace('T', ' ')
        new_type = request.form.get('popup_amount_plus')
        new_amount_big = str(request.form.get('popup_amount_big'))
        new_amount_small = str(request.form.get('popup_amount_small'))
        new_amount = float(new_amount_big + '.' + new_amount_small)

        id = request.form.get('popup_op_id')

        op = operation_by_id(int(id))
        op: Operation
        if op:
            if op.user.id == user.id:
                op.change(
                    type=int(new_type),
                    amount=new_amount,
                    category_id=new_category,
                    date=new_date,
                    description=new_description
                )
        else:
            Operation(
                id=int(id),
                user_id=user.id,
                type=int(new_type),
                amount=new_amount,
                category_id=new_category,
                date=new_date,
                description=new_description
            )

        return redirect('/operations')

    except Exception as e:
        print(e)
        return redirect('/')

# rows = [
#     [
#         [
#             1,  # id
#             '#ffc800', # color
#             'Такси' # name
#         ]
#     ],
#     [
#         [
#             "20 декабря 2021", # date
#             [
#                 [
#                     1, # categorie
#                     "2021-12-20 15:30", # datetime
#                     0, # type
#                     "2 500 000", # amount_big
#                     "00", # amoint_small
#                     "Mumba-Yumb a", # description
#                     "#ffc800", # color,
#                     357, # id
#                     "Такси" # category_name
#                 ]
#             ]
#         ]
#     ]
#
# ]


@app.route('/stats', methods=['GET'])
def stats_GET():
    try:
        session['last_page'] = '/stats'
        if "user_id" not in session:
            return redirect('/login')
        user = user_by_id(int(session['user_id']))
        balance = parse_amount(user.balance)
        rows = [[], [], user.id,
                balance,
                [
                    # Старый калькулятор инфляции был временно заменён статичным (срок работы: фев - апр 2022) из-за проблем с хостинг-сервером
                    # parse_amount(balance_by_inf(user.balance, 0)),
                    # parse_amount(balance_by_inf(user.balance, 1)),
                    # parse_amount(balance_by_inf(user.balance, 2))
                    (0, 0),
                    (0, 0),
                    (0, 0)
                ]]
        for ctg in categories:
            ctg: Category
            if ctg.user.id == user.id:
                rows[0].append([
                    ctg.id,
                    ctg.color,
                    ctg.name
                ])

        for op in operations:
            op: Operation
            if op.user.id == user.id:
                rows[1].append([
                    op.id,
                    op.type,
                    op.category.id,
                    str(op.date),
                    op.amount
                ])

        return render_template('stats.html', rows=rows)
    except Exception as e:
        print(e)
        return redirect('/')

@app.route('/categories', methods=['GET'])
def categories_GET():
    try:
        session['last_page'] = '/categories'
        if "user_id" not in session:
            return redirect('/login')
        user = user_by_id(int(session['user_id']))

        last_ctg_id = 0
        if len(categories) > 0:
            last_ctg_id = categories[-1].id + 1

        rows = [[], last_ctg_id]
        for ctg in categories:
            ctg: Category
            if ctg.user.id == user.id:
                rows[0].append([ctg.id, ctg.name, ctg.color])

        return render_template('categories.html', rows=rows)
    except Exception as e:
        print(e)
        return redirect('/')

@app.route('/categories', methods=['POST'])
def categories_POST():
    try:
        session['last_page'] = '/categories'
        if "user_id" not in session:
            return redirect('/login')
        user = user_by_id(int(session['user_id']))

        new_name = request.form.get("popup_name_input")
        new_color = request.form.get("popup_color_input")
        id = int(request.form.get("popup_id"))

        ctg = category_by_id(id)

        if ctg:
            ctg: Category
            if ctg.user.id == user.id:
                ctg.change(new_name, new_color)

        else:
            Category(id, user.id, new_name, new_color)

        return redirect('/categories')
    except Exception as e:
        print(e)
        return redirect('/')


@app.route('/download_statistic/from=<start_date>&to=<finish_date>&format=<format>')
def download_stat(start_date, finish_date, format):
    try:
        session['last_page'] = '/stats'
        if "user_id" not in session:
            return redirect('/login')
        user = user_by_id(int(session['user_id']))

        start_date = str_to_date(start_date)
        finish_date = str_to_date(finish_date)

        data = {
            "ID": [],
            "Категория": [],
            "Тип операции": [],
            "Сумма (руб)": [],
            "Описание": [],
            "Дата": []
        }

        for op in operations:
            op: Operation
            if (op.user.id == user.id and
                start_date <= op.date.date() <= finish_date):
                data["ID"].append(op.id)
                data["Категория"].append(op.category.name)
                data["Тип операции"].append("+" if op.type else "-")
                data["Сумма (руб)"].append(op.amount)
                data["Описание"].append(op.description)
                data["Дата"].append(op.date.strftime("%Y-%m-%d"))

        df = pd.DataFrame(data)

        name = f"{user.id}.{format}"


        if format == 'csv':
            df.to_csv(rf"{CURRENT_PATH}/static/exports/{user.id}.csv",
                      encoding='utf-8-sig', sep='\t', index=False)
        elif format == 'xlsx':
            df.to_excel(rf"{CURRENT_PATH}/static/exports/{user.id}.xlsx",
                        encoding='utf-8')
        else:
            return redirect("/")

        return render_template("download.html", rows=[name])
    except Exception as e:
        print(e)
        return redirect('/')


@app.route('/profile', methods=['GET'])
def profileGET():
    try:
        session['last_page'] = '/profile'
        if "user_id" not in session:
            return redirect('/login')
        user = user_by_id(int(session['user_id']))
        user: User

        rows = [
            user.name,
            user.balance,
            user.email
        ]

        return render_template('profile.html', rows=rows, error=0)
    except Exception as e:
        print(e)
        return redirect('/')

@app.route('/profile', methods=['POST'])
def profilePOST():
    try:
        session['last_page'] = '/profile'
        if "user_id" not in session:
            return redirect('/login')
        user = user_by_id(int(session['user_id']))
        user: User

        new_name = request.form.get('edit_name')
        new_balance = request.form.get('edit_balance')
        new_login = request.form.get('edit_login')
        old_password = request.form.get('old_password')
        new_password_1 = request.form.get('new_password_1')
        new_password_2 = request.form.get('new_password_2')

        if not new_password_1:
            new_password_1 = None
            new_password_2 = None

        if new_name == user.name:
            new_name = None

        if new_login == user.email:
            new_login = None

        if new_balance == user.balance:
            new_balance = None

        old_user = user_by_email(new_login)
        if (old_user or user.password != old_password
            or new_password_1 != new_password_2):
            rows = [
                user.name,
                user.balance,
                user.email
            ]
            if old_user:
                return render_template('profile.html', rows=rows,
                                       error="Ошибка! Пользователь с таким логином уже существует!")
            elif user.password != old_password:
                return render_template('profile.html', rows=rows,
                                       error="Ошибка! Введенный пароль не совпадает с текущим!")
            else:
                return render_template('profile.html', rows=rows,
                                       error="Ошибка! Введенные пароли не совпадают!")

        else:
            user.change(
                new_name,
                new_login,
                new_password_1,
                new_balance
            )
        return redirect('/profile')
    except Exception as e:
        print(e)
        return redirect('/')

@app.route('/logout')
def logout():
    session['last_page'] = '/'
    session.pop('user_id')
    return redirect('/')