# Финансовый контролер

## О проекте
Это приложение, разработанное для предпрофессиональной 
олимпиады 2022 (кейс НИУ ВШЭ).

В данный момент доступен по адресу 
http://4ashk1n.pythonanywhere.com/

Демонстрация работы: 
https://www.youtube.com/watch?v=EZGHHzGjdt0

## Использование

### Авторизация
- Первым делом вы должны войти в свой аккаунт 
или зарегистрироваться на сайте
- Страница авторизации откроется сразу, как только
вы попробуете открыть какую-нибудь вкладку
(кроме вкладки "Информация")
- Когда вы введете правильные логин и пароль
(или зарегистрируетесь), вы будете переадресованы на
вкладку, которую вы хотели посетить изначально

### Категории
- Каждая операция имеет категорию, к которой она
принадлежит. Поэтому, прежде чем добавлять операции,
необходимо создать категории
- Чтобы создать категорию, нажмите кнопку "Новая категория"
- Чтобы отредактировать существующую категорию, нажмите
кнопку "Редактировать" внутри ячейки с выбранной категорией
- Перед вами появится всплывающее окно. Вы изменить название
категории в поле для ввода текста. Также вы можете выбрать цвет
для категории, нажав на шапку окна

### Операции
- Чтобы добавить операцию, нажмите кнопку "Добавить операцию"
- Чтобы узнать подробную информацию об операции или отредактировать
ее, нажмите на ячейку с нужной операцией
- Появится всплывающее окно
- Чтобы изменить данные об операции, нажмите на кнопку в виде
карандаша, которая находится около названия категории операции
- Вы можете изменить категорию, к которой относится операция,
описание операции, дату и время, а также тип операции и сумму
- Чтобы сохранить введенные данные, нажмите на кнопку в виде
галочки в правой верхней части всплывающего окна
- На левой стороне страницы находятся фильтры и данные о балансе
- Фильтры применяются автоматически при их изменении
- В нижней части блока с фильтрами находится кнопка-переключатель
"Режима базовой операции"
    - Когда этот режим активирован, вам надо выбрать операцию,
    сумма которой станет базовой для пересчета сумм
    остальных операций и баланса
    - Суммы операций пересчитаются в условных единицах -
    суммах выбранной операции
    - _Например: вы потратили 150 рублей в супермаркете и
    1,500 рублей в салоне красоты. Если вы выберете первую
    операцию в качестве базовой, сумма второй станет
    равной 10 условным единицам_
   
### Статистика
- #### Круговые диаграммы
    - Показывают общие траты по категориям
    - Могут быть отфильтрованы по категориям и датам
    - Если навести на определенный цвет, появится общее
    значение трат по данной категории
- #### Баланс относительно инфляции
    - На левой стороне страницы есть блок с балансом, 
    расчитанным относительно инфляции за 3, 6 и 12 месяцев
    - Данные об инфляции взяты только для России
- #### Экспорт данных
    - Вы можете экспортировать данные о своих операциях
    за определенный временной период
    - Чтобы выбрать формат экспортированного файла, нажмите
    на одну из двух кнопок: _*.xlsx_ или _*.csv_
- #### Прогноз расходов на текущий месяц
    - Прогноз расходов составляется при помощи линейной регрессии
    - Над диаграммой написан общий прогноз на конец текущего 
    месяца. Вы можете также посмотреть прогноз на каждый
    из дней месяца, если наведете на определенную точку
    на графике линейной регрессии

### Мой профиль
- На этой странице вы можете редактировать данные 
о своем профиле
- Чтобы выйти из аккаунта, нажмите красную кнопку
"Выйти" в правой верхней части страницы
- Чтобы сохранить любые изменения в данных об
аккаунте, необходимо ввести свой текущий пароль 
в правое верхнее поле для ввода и нажать кнопку
"Сохранить изменения"


---
# Finance controller

## About
This is an application developed
for the Pre-Professional Olympiad 2022.

Currently located at
http://4ashk1n.pythonanywhere.com/

Demo video:
https://www.youtube.com/watch?v=EZGHHzGjdt0
## Usage

### Authorization
- First of all, you need to log in or 
create an account on the website.
- The authorization page will open as soon 
as you try to go to any tab (except "Info" tab)
- When you enter the correct username and password 
(or register), you will be redirected to the tab 
you wanted to visit 

### Categories
- Each operation has a category to which it belongs. 
Therefore, before adding transactions, you need to 
create categories
- To create a category, click the "New category" 
_("Новая категория")_ button
- To edit an existing category, click the "Edit" _("Редактировать")_
 button in the cell of the category you want to edit
- A pop-up window will open in front of you.
 You can enter the name of the category 
 in the text input field, and also choose 
 the color for the category by clicking on 
 the topbar
 
 ### Transactions
- To add an transaction, click the "Add transaction" 
_("Добавить операцию")_ button
- To read more about an transaction or edit it, click 
on the cell of the transaction you want to interact with
- A pop-up window will open in front of you.
- To edit an transaction, click on the pencil next to
 name of the category of the transaction
- You can change the category to which the transaction belongs, 
the description of the transaction, the date and time, as well 
as the type and amount
- To save the entered data, click on the checkmark button in 
the upper right part of the pop-up window
- On the left side of the page there are filters and a balance indicator
- Filters are applied automatically when they are changed
- At the bottom of the filter box is the "Basic Operation Mode" 
switch button
    - When this mode is activated, you should select and click on 
    a transaction, the amount of which will become the basis 
    for recalculating the amounts of other transactions and the balance
    - Transaction amounts will be measured in arbitrary units - the 
    amount of the selected operation
    - _For example: you spent 150 RUB on a supermarket and 
    1,500 RUB on a beauty salon. When choosing the first 
    transaction as the base one, the amount of the second 
    one will become equal to 10 conventional units_

### Statistics

- #### Pie diagrams
    - Display total expenses by different categories
    - They can be filtered by categories and dates
    - When hovering, the total expense by category is shown

- #### Balance relative to inflation
    - On the left side of the page there is a box with a 
    balance calculated relative to inflation for 3, 6 and 
    12 months
    - Inflation data is taken for Russia only

- #### Data export
    - You can export data about your operations for a certain 
    time period
    - There are two buttons here that define the file format 
    to which the data is exported: _*.xlsx_ and _*.csv_
    
- #### Cost forecast for the current month
    - Expenses for the current month are predicted using 
    linear regression
    - Above the graph, a general forecast for the end of 
    the month is written. You can also see the forecast 
    for each day of the month by hovering over the point
     of the linear regression graph

### My Profile
- On this page you can edit your profile information
- To log out of your account, you must click on the 
red "Logout" _("Выйти")_ button
- To save any changes to your account, you must enter 
your current account password in the upper right input
 field and click the "Save changes" _(Сохранить изменения)_ button
 
 