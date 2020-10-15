#!/usr/bin/python3

import sqlite3
import requests as req
import print_backups as myprint
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
        status_code INTEGER,
        payload TEXT UNIQUE
        );
    ''')

    s = req.session()

    fh=open(payload_file)
    for line in fh:
        line = line.strip()
        print(line)
        r = s.get(url+line)
        if r.status_code != 404:
            print("found:",line,r.status_code)
            cur.execute('INSERT OR IGNORE INTO '+table_name+'(payload,status_code) values(?,?)',(line,r.status_code))
            conn.commit()

    myprint.print_all(table_name)

if __name__ == "__main__":
    start()