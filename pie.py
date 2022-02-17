# ПРИМЕР РАБОТЫ С MATPLOTLIB

import matplotlib.pyplot as plt
import datetime as dt

#labels =  # Названия кусочков
#sizes = [400, 12, 12, 123] # Размеры/Значения кусочков
#colors = unik_sth(filtered_ops_color) # Цвета кусочков

#f, a = plt.subplots()

#a.pie(sizes, labels=labels, colors=colors)
#a.axis('equal')

# plt.savefig('aboba.png') # Сохранить диаграмму
#plt.show() # Предпросмотр диаграммы

# ==============================================================================

users = []
categories = []
operations = []

class User:
    id: int
    email: str
    password: str
    name: str
    reg_date: dt.date
    def __init__(self, id, email, password, name, reg_date=None,
                 new = True):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

        if reg_date:
            self.reg_date = str_to_date(reg_date)
        else:
            self.reg_date = dt.datetime.now().date()

        users.append(self)

class Category:
    id: int
    user: User
    name: str
    color: str
    def __init__(self, id, user_id, name, color,
                 new = True):
        self.id = id
        self.user = user_by_id(user_id)
        self.name = name
        self.color = color

        categories.append(self)

class Operation:
    id: int
    user: User
    types: int
    amount: float
    category: Category
    date: dt.datetime
    description: str
    def __init__(self, id, user_id, types, amount, category_id, date=None, description=None,
                 new=True):
        self.id = id
        self.user = user_by_id(user_id)
        self.type = types
        self.amount = amount
        self.category = category_by_id(category_id)

        if date:
            self.date = date
        else:
            self.date = dt.datetime.now()

        self.description = description

        operations.append(self)

def user_by_id(id):
    for usr in users:
        if usr.id == id:
            return usr
    return None

def category_by_id(id):
    for ctg in categories:
        if ctg.id == id:
            return ctg
    return None

usr = User(id=0, email='ggg@gmail.ru', password="12345", name="Dmitry")

Category(id=0, user_id=0, name="Фастфуд", color="#FFAA00")
Category(id=1, user_id=0, name="Супермаркеты", color="#133CAC")
Category(id=2, user_id=0, name="Аптеки", color="#E3669E")
Category(id=3, user_id=0, name="Транспорт", color="#667BC6")
Category(id=4, user_id=0, name="Книги", color="#FFA273")
Category(id=5, user_id=0, name="Переводы", color="#BAEC6A")

Operation(id=0, user_id=0, types=0, amount=100, category_id=3, date=dt.datetime(2020, 3, 8, 12, 0, 0))
Operation(id=1, user_id=0, types=0, amount=250, category_id=1, date=dt.datetime(2020, 3, 9, 15, 0, 0))
Operation(id=2, user_id=0, types=1, amount=300, category_id=5, date=dt.datetime(2020, 3, 5, 18, 0, 0))
Operation(id=3, user_id=0, types=0, amount=150, category_id=4, date=dt.datetime(2020, 3, 7, 16, 30, 0))
Operation(id=4, user_id=0, types=1, amount=100, category_id=5, date=dt.datetime(2020, 3, 8, 14, 30, 0))
Operation(id=5, user_id=0, types=0, amount=140, category_id=3, date=dt.datetime(2020, 3, 2, 12, 0, 0))
Operation(id=6, user_id=0, types=0, amount=200, category_id=2, date=dt.datetime(2020, 3, 8, 11, 0, 0))
Operation(id=7, user_id=0, types=0, amount=100, category_id=3, date=dt.datetime(2020, 3, 8, 12, 0, 0))
Operation(id=8, user_id=0, types=1, amount=120, category_id=5, date=dt.datetime(2020, 3, 12, 12, 0, 0))
Operation(id=9, user_id=0, types=0, amount=90, category_id=4, date=dt.datetime(2020, 3, 10, 12, 0, 0))

filters = {
    "user": 0,
    "type": 0,
    "categories": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "dates": (dt.datetime(2020, 3, 2, 12, 0, 0), dt.datetime(2020, 3, 20, 12, 0, 0))
}


def createDiagram(name, filters):
    # operations объявлен вне функции, использовать его
    # code
    filtered_ops = [] #Отфильтрованный массив операций
    categories_name = [] # Для ориг. назвний
    categories_color = [] # Для ориг. цвета
    categorys_size_list = []
    categorys_size = {}
    l = []
    
    for id in filters["categories"]:
        categorys_size[id] = 0

    for op in operations:
        if op.type == filters["type"] and op.user.id == filters["user"] and op.category.id in filters["categories"] and filters["dates"][0]<=op.date<=filters["dates"][1]:
            categorys_size[op.category.id] += op.amount
    for id in categorys_size:
        if categorys_size[id]!=0:
            categorys_size_list.append(categorys_size[id])
            cat = category_by_id(id)
            categories_name.append(cat.name)
            categories_color.append(cat.color)
 
    f, a = plt.subplots()

    wedges, texts = a.pie(categorys_size_list,
                          wedgeprops=dict(width=0.5),
                          colors=categories_color,
                          center=(0.3, 0.5))
    a.axis('equal')
    # a.legend(wedges, categories_name,
    #          title="Категории", loc="lower center",
    #          fontsize='large', title_fontsize="large")
    f.set_size_inches(3, 3)
    plt.savefig(name + '.svg',) # Сохранить диаграмму
    # plt.show() # Предпросмотр диаграммы

createDiagram("hfh", filters)
            



'''
Функция создает файл с диаграммой, на которой изображены 
категории, размер каждой из которых зависит от количества
денег, использованных в данной категории.    

name - имя файла, который нужно будет создать

operations - массив операций
Пусть op - операция
op.amount - количество денег в операции
op.category.id - ID категории для этой операции
op.category.name - название категории 
op.type - тип операции. 0 - списание, 1 - пополнение
op.category.color - цвет для данной категории
op.date - дата (тип данных - datetime.datetime)

filters - словарь фильтров
{
    "user": <ID пользователя>,
    "type": <0 или 1>,
    "categories": <массив из ID-шников различных категорий>,
    "dates": <кортеж из двух элементов - начальная дата и конечная (datetime.datetime)>
}
Необходимо, чтобы все использованные операции соответствовали каждому из фильтров
- Айди пользователя должны совпадать с айди из фильтров
- Типы должны совпадать с типом из фильтра
- айди категории должен лежать в массиве категорий из фильтров
- дата должна находиться в промежутке между начальной и конечной (включительно) из фильтров 

Установка сторонних библиотек (гайд):
https://pythonru.com/uroki/python-pip-uroki-po-python-dlja-nachinajushhih

Тебе понадобится библиотека matplotlib, её нужно скачать
'''
