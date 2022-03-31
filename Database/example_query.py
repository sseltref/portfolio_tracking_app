import sqlite3
from sqlite3 import Error

def create_connection(db):
	conn = None

	try:
		conn = sqlite3.connect(db)
	except Error as e:
		print(e)

	return conn

def make_transaction(conn, tr_date, currency1, currency2, volume, value):
	cur = conn.cursor()
	cur.execute('INSERT INTO history(tr_date, currency1, currency2, volume, value) VALUES (?, ?, ?, ?, ?)', (tr_date, currency1, currency2, volume, value))
	conn.commit()

''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''

conn_tr = create_connection('database.db')
make_transaction(conn_tr, '31-03-2022', 'USD', 'PLN', 100, 450)