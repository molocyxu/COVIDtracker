from defines import *
from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
from flask import g
import time
import sqlite3
#import update_records
import os
import csv

DATABASE= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset.db')
def connect_db():
    return sqlite3.connect(DATABASE)

def close_db():
    if hasattr(g, '_db'):
        g._db.close()

def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db

app = Flask(__name__)
#def app_init():
    #g.db = get_connection()
#    update_records.update_text()
#    app.stus = update_records.get_map()
def query_db(query, args=()):
    with sqlite3.connect(DATABASE) as db:
        cur = db.execute(query, args)
        rv = [dict((cur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in cur.fetchall()]
        #close_db()
        #print(rv)
        return rv


#app_init()


import random

def random_distribution(amount,rand_num=5, border=10):
    list1 = []
    for i in range(0,rand_num-1):
        #print(border, amount)
        a = random.randint(-border,amount)
        list1.append(a)
    list1.sort()
    list1.append(amount)

    list2 = []
    for i in range(len(list1)):
        if i == 0:
            b = list1[i]
        else:
            b = list1[i] - list1[i-1]
        list2.append(b)
    return list2

def algorithm(test_results, rand_num=5, border=10):
    aggregator = 0
    total_num = len(test_results)
    dist_results = [0]*total_num
    for i in range(total_num):
        p_i = test_results[i]
        rand_list=random_distribution(p_i, rand_num, border)
        rand_p_list = random.sample(range(0, total_num), rand_num)
        for j in range(len(rand_p_list)):
            dist_results[rand_p_list[j]] += rand_list[j]
    aggregator = sum(dist_results)
    return aggregator, total_num

def get_results_in_region(region):
    results = []
    #print(region)
    try:
        recordings = query_db('select * from dataset where region = ?', [region])
        for record in recordings:
            results.append(record['result'])
    except Exception:
        return None

    if len(results) == 0:
        return None
    return results

def insert_recordings(region, result):
    try:
        query_db('insert into dataset values(?, ?)', [region, result])
        return True
    except Exception:
        return False

def check_update_time():
    now_time = time.time()
    n_time = time.localtime(now_time)
    ret = time_str % (n_time.tm_year, n_time.tm_mon, n_time.tm_mday, n_time.tm_hour, n_time.tm_min, n_time.tm_sec)
    return ret

@app.route('/', methods=['GET'])
def home():
    update_time = check_update_time()
    return render_template('index.html', error_query=0, update_time=update_time)

@app.route('/retry', methods=['GET'])
def retry():
    update_time = check_update_time()
    return render_template('index.html', error_query=1, update_time=update_time)

@app.route('/error', methods=['GET'])
def error():
    update_time = check_update_time()
    return render_template('update.html', miss_query=1, update_time=update_time)

@app.route('/fail', methods=['GET'])
def fail():
    update_time = check_update_time()
    return render_template('update.html', fail_query=1, update_time=update_time)


@app.route('/success', methods=['GET'])
def success():
    update_time = check_update_time()
    return render_template('update.html', success_query=1, update_time=update_time)

@app.route('/update', methods=['GET'])
def update():
    update_time = check_update_time()
    return render_template('update.html', error_query=0, update_time=update_time)

@app.route('/query', methods=['GET'])
def query():
    region = request.args.get('region', None)
    region = region.lower()
    results = get_results_in_region(region)
    #print(results)
    if results is None:
        return redirect('/retry')
    else:
        aggregator, total_num = algorithm(results, min(len(results), 5))
        report = UniObject()
        report.aggregator = aggregator
        report.total_num = total_num
        report.region = region.upper()
        #print(aggregator, total_num, region)
        return render_template('query.html', report=report)

@app.route('/insert', methods=['GET','POST'])
def insert():
    region = request.form.get('region', '')
    region = region.lower()
    result = request.form.get('result', '')
    if result == '' or region == '':
        return redirect('/error')
    else:
        succ = insert_recordings(region, result)
        if succ:
            return redirect('/success')
        else:
            return redirect('/fail')

if __name__ == '__main__':
    app.run()
