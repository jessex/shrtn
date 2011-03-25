import sqlite3 as sql

LOCATION = "shrtn/db"
MYTABLE = "urls"

def setup_sql():
	"""Establishes a connection to the sqlite database at LOCATION and returns 
	the database connection object."""
	try:
		conn = sql.connect(LOCATION)
		return conn
	except sql.OperationalError:
		print "Error: could not open database file"
		return None

def table_exists(table, conn):
	"""Returns whether or not the table exists in the database at conn."""
	result = conn.execute('select name from sqlite_master where name=?', \
	(table,))
	return not (not result.fetchall()) #False if does not exist, True otherwise

def create_table(table, conn):
	pass


