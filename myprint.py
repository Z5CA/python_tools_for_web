#!/usr/bin/python3

import sqlite3
from myinit import *

def start():
    global table_name
    
    conn=sqlite3.connect(db_file_name+'.sqlite')
    cur = conn.cursor()
    print('Tables are : ')
    for row in cur.execute('select name from sqlite_master where type = "table" and name not like "sqlite_%";'):
        print(row[0],end=', ')
    cur.close()
    print()
    print()
    ip = input("Enter table name to print : ")
    if ip != '':
        table_name = ip
    print_all(table_name)

def print_all(tbname):
    conn=sqlite3.connect(db_file_name+'.sqlite')
    cur =conn.cursor()

    sqlstr='select * from '+tbname

    try:
        cur.execute(sqlstr)
        colnames = [description[0] for description in cur.description]
        print('')
        print('Here is table ('+table_name+')')
        print('\n---------------------------------')
        print('\t|'.join(colnames))
        print('---------------------------------')
        for row in cur:
            print('\t|'.join(str(r) for r in row))
        print('---------------------------------')
        cur.close()
    except:
        print('Error')

if __name__ == "__main__":
    start()