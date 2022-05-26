import sqlite3
from example_query import create_connection
import yfinance as yf
import datetime
import random

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

def import_tickers():
	ticker = {}
	conn = create_connection('tickers.db')
	cur = conn.cursor()
	
	cur.execute(f"SELECT * FROM tickers")

	for line in cur.fetchall():
		ticker[line[0]] = line[1]

	return ticker

def portfolio_value():
	values, v = {}, 0
	conn = create_connection('database.db')
	cur = conn.cursor()
	
	cur.execute(f"SELECT * FROM history")
	operations = sorted(cur.fetchall(), key=lambda x: x[1])

	conn.close()

	ticker = import_tickers()
	#print(ticker)

	for line in operations:
		date = datetime.datetime.fromtimestamp(line[1]).strftime('%Y-%m-%d')
		#print(line)
		'sell part'
		try:
			if line[2] == 'USD':
				outcome = float(line[4])
			else:
				x = yf.download(ticker[line[2]], date, date)
				outcome = x['Close'].tolist()[0] * float(line[4])
				#print(outcome)

			y = yf.download(ticker[line[3]], date, date)
			income = y['Close'].tolist()[0] * float(line[4])

			v += round(income - outcome, 2)
			values[line[1]] = v

		except:
			continue

	return values
	#returns historical value ins USD of all assets in portfolio as a dictionary (key - date in epoch)


def transactions_list(ticker=None):
	conn = create_connection('database.db')
	cur = conn.cursor()

	
	if ticker == None:
		trans = []
		cur.execute(f"SELECT * FROM history")
		operations = sorted(cur.fetchall(), key=lambda x: x[1])

		for line in operations:
			trans.append([datetime.datetime.fromtimestamp(line[1]).strftime('%Y-%m-%d'), line[2], line[3], float(line[4])])
		return trans

	else:
		trans = {}
		trans['buy'] = []
		trans['sell'] = []
		cur.execute(f"SELECT * FROM history WHERE currency1='{ticker}'")
		operations = sorted(cur.fetchall(), key=lambda x: x[1])

		for line in operations:
			trans['sell'].append([datetime.datetime.fromtimestamp(line[1]).strftime('%Y-%m-%d'), line[2], line[3], float(line[4])])

		cur.execute(f"SELECT * FROM history WHERE currency2='{ticker}'")
		operations = sorted(cur.fetchall(), key=lambda x: x[1])

		for line in operations:
			trans['buy'].append([datetime.datetime.fromtimestamp(line[1]).strftime('%Y-%m-%d'), line[2], line[3], float(line[4])])

		return trans
	#returns dictionary with all transactions of given ticker (sorted by date)
	#in case of default ticker, function returns all transactions in data order

def news(n=3):
	to_export = []
	assets = assets_to_sell()

	conn = create_connection('tickers.db')
	cur = conn.cursor()

	cur.execute(f"SELECT * FROM tickers")

	for line in cur.fetchall():
		a = yf.Ticker(line[1])
		if len(a.news) < 1:
			continue
		else:
			to_export.append([a.news[0]['title'], a.news[0]['link'], datetime.datetime.fromtimestamp(a.news[0]['providerPublishTime']).strftime('%Y-%m-%d')])

	return random.sample(to_export, n)
	#returns random n (default n=3) news as a list


print(portfolio_value())