# import csv
# from datetime import date
from math import ceil

from flask import Flask, render_template, request
# from numpy import var
# from sqlalchemy import DATETIME
# from werkzeug.utils import redirect

app = Flask(__name__)
# import sqlite3 as sql
# import pandas as pd
# dbc = sql.connect('database.db')
# dataframe1 = pd.read_csv('edata.csv')
# Referenced from https://stackoverflow.com/questions/43730422/how-to-split-one-column-into-multiple-columns-in-pandas-using-regular-expression
# dataframe1[['date', 'time'] ]= dataframe1['time'].str.split('T', expand=True)
# dataframe1[['time']]= dataframe1['time'].str.split('.').str[0]
# dataframe1.to_sql('testtable1', dbc, if_exists='replace')


@app.route('/')
def home():
   return render_template("homescreen.html")

@app.route('/go')
def go():
   return render_template("home.html")


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("Select * from testtable1;")
    rows4 = cur.fetchall()
    return render_template("home.html", rows4=rows4)

@app.route('/query1', methods=['POST'])
def query1():
    eq = request.form['mag']
    eq1 = request.form['maga']
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur1 = con.cursor()
    cur2 = con.cursor()
    cur3 = con.cursor()
    cur1.execute('select * from testtable1 where gap <? ;', (eq,))
    cur2.execute('select * from testtable1 where gap>? ;', (eq1,))
    cur3.execute('select * from testtable1 where gap between ? and ? ;', (eq,eq1,))
    rows1 = cur1.fetchall()
    rows1a = cur2.fetchall()
    rows1b= cur3.fetchall()
    total1 = 0
    totala = 0
    totalb = 0
    for row in rows1:
     total1 = total1 + 1
     for row in rows1a:
      totala = total1 + 1
     for row in rows1b:
      totalb = total1 + 1
    return render_template('home.html', total1=total1, totala=totala, totalb=totalb)


@app.route('/query2', methods=['POST'])
def query2():
    a = request.form['query2a']
    b = request.form['query2b']
    c = request.form['query2c']
    d = request.form['query2d']
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('select * from testtable1 where mag BETWEEN ? AND ? AND date BETWEEN ? AND ?;', (a,b,c,d,))
    rows2 = cur.fetchall()
    total2 = 0
    for row in rows2:
        total2 = total2 + 1
    return render_template('home.html', total2=total2, rows2=rows2)

@app.route('/query3', methods=['POST'])
def query3():
    a = request.form['query3a']
    a=float(a)
    b = request.form['query3b']
    b = float(b)
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    #Referenced from https://stackoverflow.com/questions/10318002/20-km-miles-around-a-lat-long
    distanceKilometers=float(1000.000)
    difference =float( 0.070)
    distance = float(ceil (distanceKilometers / 111))
    latitude_from = float(a - difference - distance)
    latitude_to = float(a + difference + distance)
    longitude_from = float(b - difference - distance)
    longitude_to =float(b + difference + distance)
    cur.execute('select latitude,longitude from testtable1 where latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?;', (latitude_from,latitude_to,longitude_from,longitude_to,))
    rows3 = cur.fetchall()
    total3 = 0
    for row in rows3:
        total3 = total3 + 1
    return render_template('home.html', total3=total3, rows3=rows3)

@app.route('/query5', methods=['POST'])
def query5():
    a = request.form['query5a']
    b = request.form['query5b']
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('select time,latitude,longitude,place from testtable1 where mag>? and place like \'%'+a+'%\';', (b,))
    rows5 = cur.fetchall()
    return render_template('home.html', rows5=rows5)

if __name__ == '__main__':
    app.run(debug=True)
