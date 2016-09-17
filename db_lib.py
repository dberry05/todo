import sqlite3, json
from datetime import datetime

#DB = '/app/db/home.db'
DB = '/media/data/data/site/db/home.db'


def execute_query(query):
    con = sqlite3.connect(db)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(query)
    data = cur.fetchall()


def get_all_tasks(DB, query):
    return execute_query(query)
          


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
def get_all_tasks():
    ''' Gets active tasks from todo database and returns json string'''
    con = sqlite3.connect(DB)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select * FROM todo")
    my_data =  cur.fetchall()
    return [item for item in my_data]

def get_active_tasks():
    ''' Gets active tasks from todo database and returns json string'''
    con = sqlite3.connect(DB)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select * FROM todo where status ='open'")
    my_data =  cur.fetchall()
    return [item for item in my_data]
	
def get_regular_tasks():
    ''' Gets active tasks from todo database and returns json string'''
    con = sqlite3.connect(DB)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select * FROM todo where status ='open' AND type !='things i want' AND type != 'things we want' AND type != 'computer' ")
    my_data =  cur.fetchall()
    return [item for item in my_data]
	
def get_types():
    ''' Gets task categories tasks from todo database and returns json string'''
    con = sqlite3.connect(DB)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select DISTINCT(type) FROM todo")
    my_data =  cur.fetchall()
    return [item['type'] for item in my_data]

def get_tasks_by_type(type_name):
    ''' Gets active tasks from a given type from todo database and returns json string'''
    con = sqlite3.connect(DB)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select * FROM todo where status ='open' AND type='"+ type_name + "'")
    my_data =  cur.fetchall()
    return [item for item in my_data]

def create_task(task):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO todo (type, item, date_opened, status) VALUES (?, ?, ?, ?)", (task['type'], task['item'], task['date_opened'], task['status']))
    new_id = c.lastrowid
    conn.commit()
	
def update_task(task):
    if task['status'] == 'closed':
        task['date_closed'] = datetime.now()
    format_sql = ', '.join(["{}='{}'".format(k,v) for k,v in task.items()])
    SQL="UPDATE todo SET %s WHERE id=%s" % (format_sql, task['id'])
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
