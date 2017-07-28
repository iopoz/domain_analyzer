import os
import re
import sqlite3 as db_driver
import time
from datetime import datetime, timedelta
import datetime as dt_class


def connect():
    db_path = os.path.join(os.path.abspath(''), "storage.db")
    db = db_driver.connect(db_path)
    cur = db.cursor()
    try:
        cur.execute('SELECT * from domains')
    except:
        cur.execute('CREATE TABLE domains('
                    'domain_id INTEGER PRIMARY KEY,'
                    'domain_key TEXT,'
                    'domain_white INTEGER);')
    return db


def terminate(db):
    try:
        if db:
            db.close()
    except db_driver.Error as e:
        print('Error %s:' % e.args[0])


def add_new_domain(domain_list):
    db = connect()
    cur = db.cursor()
    for domain in domain_list:
        cur.execute('SELECT domain_key FROM domains WHERE domain_key = ?', [domain])
        row = cur.fetchall()
        if row:
            print('domain %s was added before' % domain)
        else:
            cur.execute('INSERT INTO domains (domain_key, domain_white) VALUES(?, ?)', (domain, 0))
            db.commit()
    terminate(db)


def get_domains_by_name(value):
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT domain_key FROM domains WHERE domain_key LIKE ?", ['%' + value + '%'])
    data = cur.fetchall()
    terminate(db)
    return data


def mark_as_white(white_list):
    db = connect()
    cur = db.cursor()
    for value in white_list:
        cur.execute("UPDATE domains SET domain_white = 1 WHERE domain_key = ?", [value])
        db.commit()
    terminate(db)


def mark_as_black(white_list):
    db = connect()
    cur = db.cursor()
    for value in white_list:
        cur.execute("UPDATE domains SET domain_white = 2 WHERE domain_key = ?", [value])
        db.commit()
    terminate(db)


def get_domains_for_driver(value):
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT domain_key FROM domains WHERE domain_key LIKE ? AND domain_white = 2", ['%' + value + '%'])
    data = cur.fetchall()
    terminate(db)
    return data
