import sqlite3
from sqlite3 import Error
import datetime
from random import uniform, choice

def create_connection(db):
	try:
		conn = sqlite3.connect(db)
	except Error as e:
		print(e)

	return conn

def make_transaction(conn, tr_date, currency1, currency2, volume):
	cur = conn.cursor()
	cur.execute('INSERT INTO history(tr_date, currency1, currency2, volume) VALUES (?, ?, ?, ?)', (tr_date, currency1, currency2, volume))
	conn.commit()


def last_n_days_transactions(conn, ticker, date, n):
	cur = conn.cursor()
	transactions = []
	s_date = datetime.datetime(date[0], date[1], date[2])
	for d in range(n+1):
		temp_date = (s_date + datetime.timedelta(-1*d)).strftime("%d-%m-%y")
		cur.execute(f"SELECT * FROM history WHERE currency1='{ticker}' AND tr_date LIKE '{temp_date}%'")
		#print(temp_date, cur.fetchall())
		transactions += cur.fetchall()
	
	return transactions


def random_transactions(n):
	currencies = ['USD', 'PLN', 'EUR', 'CHF', 'GBP', 'BTC']
	for _ in range(n):
		x = datetime.datetime(int(uniform(2019,2023)), int(uniform(1,13)), int(uniform(1,29)), int(uniform(0,24)), int(uniform(0,60)), int(uniform(0,60)))
		c1 = choice(currencies)
		while True:
			c2 = choice(currencies)
			if c2 != c1:
				break
		vol = round(uniform(0, 10000),2)
		#print(vol)
		#make_transaction(conn_tr, x.strftime("%d-%m-%y %H:%M:%S"), c1, c2, vol)
		print(conn_tr, int(x.timestamp()), c1, c2, vol)
		make_transaction(conn_tr, int(x.timestamp()), c1, c2, vol)

'''
conn_tr = create_connection('database.db')
#make_transaction(conn_tr, datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"), 'USD', 'PLN', 100)

tr = last_n_days_transactions(conn_tr, 'PLN', (2022, 4, 7), 10)
print(tr)

#

'''
'''
conn_tr = create_connection('database.db')
random_transactions(10000)
'''