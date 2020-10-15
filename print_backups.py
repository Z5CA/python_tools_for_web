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
        print('')
        print('Here is table ('+table_name+')')
        print('\n---------------------------------')
        print('id\t|status\t|filename')
        print('---------------------------------')
        for row in cur.execute(sqlstr):
            print(str(row[0]),"\t|",row[2],"\t|",row[1])
        print('---------------------------------')
        cur.close()
    except:
        print('Error')

if __name__ == "__main__":
    start()