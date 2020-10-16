#!/usr/bin/python3

import sqlite3
import requests as req
import myprint
from os import listdir
from os.path import isfile, join
from myinit import *

def start():
    global want_question
    global url
    global table_name
    global db_file_name
    global payload_path
    global payload_file
    global default_keyword
    global default_length

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

    conn=sqlite3.connect(db_file_name+'.sqlite')
    cur =conn.cursor()

    cur.execute('drop table if exists '+table_name)
    cur.execute('CREATE TABLE '+table_name+''' (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        length INTEGER,
        payload TEXT UNIQUE
        );
    ''')

    fh=open(payload_file)
    if default_length<0:
        default_length = len(req.get(url).html)

    for line in fh:
        line = line.strip()
        print(line)
        headers={
            'User-Agent':line,
        }
        r = req.get(url,headers=headers)
        len_html=len(r.html)
        if len_html!=default_length or default_keyword not in r.html:
            print("found:",line,r.status_code)
            cur.execute('INSERT OR IGNORE INTO '+table_name+'(length,payload) values(?,?)',(len_html,line))
            conn.commit()

    myprint.print_all(table_name)

if __name__ == "__main__":
    start()