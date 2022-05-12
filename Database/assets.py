import sqlite3
from example_query import create_connection

def assets_to_sell():
	export = []
	conn = create_connection('database.db')
	cur = conn.cursor()

	cur.execute("SELECT DISTINCT currency2 FROM history")

	for line in cur.fetchall():
		export.append(line[0])

	return export


