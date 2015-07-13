#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import random

con = mdb.connect(host='localhost', user='vasu', db='quizbowl', passwd='seleniumpython');
with con:
    cur = con.cursor()
    cur.execute('use quizbowl')
    cur.execute('SELECT * from tossup')
    rows = cur.fetchall()
    print rows

