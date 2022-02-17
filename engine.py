from config import *


def str_to_date(s):
    return dt.datetime.strptime(s, "%Y-%m-%d").date()

def str_to_datetime(s):
    try:
        return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except:
        try:
            return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")
        except:
            return None

def user_by_id(id):
    for usr in users:
        if usr.id == id:
            return usr
    return None

def user_by_email(email):
    for usr in users:
        usr: User
        if usr.email == email:
            return usr
    return None

def category_by_id(id):
    for ctg in categories:
        if ctg.id == id:
            return ctg
    return None

def operation_by_id(id):
    for op in operations:
        if op.id == id:
            return op
    return None


def render_date(date: dt.datetime):
    monthes = ['января', 'февраля', 'марта',
               'апреля', 'мая', 'июня',
               'июля', 'августа', 'сентября',
               'октября', 'ноября', 'декабря']

    day = str(date.day)
    month = monthes[date.month - 1]
    year = str(date.year)
    return day + " " + month + " " + year

def unrender_date(date: str):
    date = date.split()
    monthes = ['января', 'февраля', 'марта',
               'апреля', 'мая', 'июня',
               'июля', 'августа', 'сентября',
               'октября', 'ноября', 'декабря']

    day = date[0]
    month = monthes.index(date[1]) + 1
    year = date[2]
    return str_to_date(f"{year}-{month}-{day}")


def parse_amount(amount):
    amount = str(amount).split('.')
    new_big = ''
    if len(amount[0]) >= 3:
        for k in range(len(amount[0]), 0, -3):
            new_big = amount[0][k-3:k] + ' ' + new_big
    new_big = amount[0][0:len(amount[0]) % 3] + new_big
    amount[0] = new_big
    while len(amount[1]) < 2:
        amount[1] += '0'

    while amount[0][0] == ' ':
        amount[0] = amount[0][1:]

    while amount[0][-1] == ' ':
        amount[0] = amount[0][:-1]

    return amount[0], amount[1]

class User:
    id: int
    email: str
    password: str
    name: str
    balance: float
    reg_date: dt.date

    def __init__(self, id, email, password, name, balance, reg_date=None,
                 new = True):
        if id == -1:
            id = users[-1].id + 1
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.balance = balance
        self.balance = float("{0:.2f}".format(self.balance))

        if reg_date:
            self.reg_date = str_to_date(reg_date)
        else:
            self.reg_date = dt.datetime.now().date()

        self.dbUpdate(new)
        users.append(self)

    def dbUpdate(self, new=False):
        if new:
            db_cursor.execute(f'''
            INSERT INTO users VALUES 
            (
            "{self.id}",
            "{self.email}",
            "{self.password}",
            "{self.name}",
            "{str(self.reg_date)}",
            "{float(self.balance)}"
            )''')
        else:
            db_cursor.execute(f'''
            UPDATE users SET 
            email = "{self.email}",
            password = "{self.password}",
            name = "{self.name}",
            balance = "{float(self.balance)}"
            WHERE id = "{self.id}"
            ''')

        DB.commit()

    def balanceChange(self, plus):
        self.balance += plus
        self.balance = float("{0:.2f}".format(self.balance))
        self.dbUpdate()

    def change(self, name, email, password, balance):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password
        if balance is not None:
            self.balance = balance
        self.dbUpdate()


class Category:
    id: int
    user: User
    name: str
    color: str

    def __init__(self, id, user_id, name, color,
                 new = True):
        if id == -1:
            id = categories[-1].id + 1
        self.id = id
        self.user = user_by_id(user_id)
        self.name = name
        self.color = color

        self.dbUpdate(new)
        categories.append(self)

    def dbUpdate(self, new=False):
        if new:
            db_cursor.execute(f'''
            INSERT INTO categories VALUES 
            (
            "{self.id}",
            "{self.user.id}",
            "{self.name}",
            "{self.color}"
            )''')
        else:
            db_cursor.execute(f'''
            UPDATE categories SET 
            color = "{self.color}",
            name = "{self.name}"
            WHERE id = "{self.id}"
            ''')

        DB.commit()


    def change(self, name=None, color=None):
        if name is not None:
            self.name = name
        if color is not None:
            self.color = color
        self.dbUpdate()

class Operation:
    id: int
    user: User
    type: int
    amount: float
    category: Category
    date: dt.datetime
    description: str

    def __init__(self, id, user_id, type, amount, category_id, date=None, description=None,
                 new=True):
        if id == -1:
            id = operations[-1].id + 1
        self.id = id
        self.user = user_by_id(user_id)
        self.type = type
        self.amount = amount
        self.category = category_by_id(category_id)

        if date:
            self.date = str_to_datetime(date)
        else:
            self.date = dt.datetime.now()

        self.description = description

        if new:
            if self.type:
                self.user.balanceChange(self.amount)
            else:
                self.user.balanceChange(-self.amount)

        self.dbUpdate(new)
        operations.append(self)


    def dbUpdate(self, new):
        if new:
            db_cursor.execute(f'''
            INSERT INTO operations VALUES 
            (
            "{self.id}",
            "{self.user.id}",
            "{self.type}",
            "{self.amount}",
            "{self.category.id}",
            "{str(self.date)}",
            "{self.description}"
            )''')
        else:
            db_cursor.execute(f'''
            UPDATE operations SET 
            type = "{self.type}",
            amount = "{self.amount}",
            category = "{self.category.id}",
            date = "{str(self.date)}",
            description = "{self.description}"
            WHERE id = "{self.id}"
            ''')

        DB.commit()


    def change(self, type=None, amount=None, category_id=None,
               date=None, description=None):

        if amount is not None:
            if self.type:
                self.user.balanceChange(-self.amount)
            else:
                self.user.balanceChange(self.amount)

            self.amount = amount

            if self.type:
                self.user.balanceChange(self.amount)
            else:
                self.user.balanceChange(-self.amount)

        if type is not None:
            if type != self.type:
                if self.type:
                    self.user.balanceChange(-self.amount)
                else:
                    self.user.balanceChange(self.amount)
                self.type = type
                if self.type:
                    self.user.balanceChange(self.amount)
                else:
                    self.user.balanceChange(-self.amount)

        if category_id is not None:
            self.category = category_by_id(category_id)
        if date is not None:
            self.date = str_to_datetime(date)
        if description is not None:
            self.description = description
        self.dbUpdate(False)

def db_import():
    db_u = db_cursor.execute('SELECT * FROM users').fetchall()
    db_c = db_cursor.execute('SELECT * FROM categories').fetchall()
    db_o = db_cursor.execute('SELECT * FROM operations').fetchall()

    for usr in db_u:
        User(
            id = usr[0],
            email = usr[1],
            password = usr[2],
            name = usr[3],
            reg_date = usr[4],
            balance = usr[5],
            new = False
        )

    for ctg in db_c:
        Category(
            id = ctg[0],
            user_id = ctg[1],
            name = ctg[2],
            color = ctg[3],
            new = False
        )

    for op in db_o:
        Operation(
            id = op[0],
            user_id = op[1],
            type = op[2],
            amount = op[3],
            category_id = op[4],
            date = op[5],
            description = op[6],
            new = False
        )




def balance_by_inf(summ, type):

    # type = 2 # год - 2, 6 мес. - 1, 3 мес. - 0

    year2 = dt.date.today().year
    month2 = dt.date.today().month
    day2 = dt.date.today().day
    year1 = year2
    month1 = month2
    day1 = day2

    if type == 2:
        year1 -= 1

    elif type == 1:
        month1 -= 6
        if month1 <= 0:
            month1 += 12

    elif type == 0:
        month1 -= 3
        if month1 <= 0:
            month1 += 12


    request_link = (f'https://fxtop.com/ru/inflation-calculator.php?A={summ}' +
                    f'&C1=RUB&INDICE=RUCPI2000&DD1={day1}&MM1={month1}&YYYY1={year1}' +
                    f'&DD2={day2}&MM2={month2}&YYYY2={year2}')

    response = requests.get(request_link)

    response = response.content
    response = response.decode()
    soup = BeautifulSoup(response, "lxml")

    return float(soup.find("a", title="конвертация валют на дату окончания").text.split("RUB")[0].replace(' ',''))



