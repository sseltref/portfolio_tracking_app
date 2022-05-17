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


print(value('CHF'))