import database as db
import sys

def setup_db():
	"""Establishes a connection to our database and creates our table if it
	does not yet exist. Returns the connection to the database file."""
	conn = db.setup_sql()
	if conn == None: #Could not establish connection, so quit
		sys.exit()
	if not db.table_exists(db.MYTABLE, conn): #create table if not yet created
		db.create_table(db.MYTABLE, conn)
		conn.commit() #save changes
	return conn


