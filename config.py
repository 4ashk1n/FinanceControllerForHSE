from pyngrok import ngrok
from flask import Flask, render_template, request, session, redirect
import datetime as dt
import sqlite3 as sql
from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3.util.connection as urllib3_cn
import pandas as pd
import os
import random

requests.packages.urllib3.util.connection.HAS_IPV6 = False

# UNCOMMENT TO USE NGROK:
# ssh_tunnel = ngrok.connect(302)
# print(ssh_tunnel)

CURRENT_PATH = os.getcwd()
CURRENT_PATH = CURRENT_PATH.replace('\\', '/')
CURRENT_PATH = CURRENT_PATH.replace(r'\\', '/')

DB = sql.connect('DataBase.db', check_same_thread=False)

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"


users = []
operations = []
categories = []

db_cursor = DB.cursor()

"""
Создание таблиц для базы данных в случае их отсутствия 
"""
db_cursor.execute('''
CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER,
	"user"	INTEGER,
	"name"	TEXT,
	"color"	TEXT
);
''')
db_cursor.execute('''
CREATE TABLE IF NOT EXISTS "operations" (
	"id"	INTEGER,
	"user"	INTEGER,
	"type"	INTEGER,
	"amount"	REAL,
	"category"	INTEGER,
	"date"	TEXT,
	"description"	TEXT
);
''')
db_cursor.execute('''
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"email"	TEXT,
	"password"	TEXT,
	"name"	TEXT,
	"reg_date"	TEXT,
	"balance"	REAL
);
''')
DB.commit()
