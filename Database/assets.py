import sqlite3
from example_query import create_connection
import yfinance as yf


def assets_to_sell():
	export = []
	conn = create_connection('database.db')
	cur = conn.cursor()

	cur.execute("SELECT DISTINCT currency2 FROM history")

	for line in cur.fetchall():
		export.append(line[0])

	return export
	#retuns list of assets available to sell

def value(ticker=None):
	values = {}
	conn = create_connection('database.db')
	cur = conn.cursor()


	cur.execute("SELECT * FROM history")

	for line in cur.fetchall():
		c1, c2, v = line[2], line[3], float(line[4])

		if c1 not in values:
			values[c1] = 0
		else:
			values[c1] += v

		if c2 not in values:
			values[c2] = 0
		else:
			values[c2] -= v

		for line in values:
			values[line] = round(values[line], 2)

	if ticker == None:
		return values
	else:
		return values[ticker]

	#returns current value of ticker given in function parameter
	#parameter is empty default, so then output is dictionary with all available tickers

def historical_value(ticker):
	values = {}
	conn = create_connection('database.db')
	cur = conn.cursor()
	v = 0

	cur.execute(f"SELECT * FROM history WHERE currency1='{ticker}' OR currency2='{ticker}'")
	#print(cur.fetchall())
	operations = sorted(cur.fetchall(), key=lambda x: x[1])
	for line in operations:
		if line[3] == ticker:
			v -= float(line[4])
		else:
			v += float(line[4])

		values[int(line[1])] = round(v, 2)
		print(line[1], values[line[1]])
	return values
	#returns dictionary with historical values (key: data) of one ticker (given in parameter) 

historical_value('CHF')