import sqlite3 as sql

LOCATION = "shrtn/db" #location of database file
MYTABLE = "urls" #table name is case-sensitive

# ****************************** SETUP FUNCTIONS *******************************

def setup_sql():
	"""Establishes a connection to the sqlite database at LOCATION and returns 
	the database connection object."""
	try:
		conn = sql.connect(LOCATION)
		return conn
	except sqlite3.OperationalError:
		print "Error: could not open database file at '%s'" % LOCATION
		return None

def table_exists(table, conn):
	"""Returns whether or not the table exists in the database at conn."""
	result = conn.execute('select name from sqlite_master where name=?', \
	(table,))
	return not (not result.fetchall()) #False if does not exist, True otherwise

def create_table(table, conn):
	"""Attempts to create table in the database at conn. Returns whether or not
	the insert was successful."""
	query = 'create table %s (id INTEGER PRIMARY KEY, original TEXT)' % table
	try:
		conn.execute(query)
		conn.commit() #save changes
		return True
	except sqlite3.OperationalError:
		print "Error: table '%s' already exists" % table
		return False
		
# ******************************* CORE FUNCTIONS *******************************

def search_url(url, table, conn):
	"""Attempts to find a row in the table in the database conn with the given
	url. Returns its id value if it is present, returns False otherwise."""
	query = 'select * from %s where original="%s"' % (table, url)
	result = conn.execute(query).fetchall()
	if not result: #url not in our database, return False
		return False
	else:
		return result[0][0] #return the id of the url
	
def search_id(id, table, conn):
	"""Attempts to find a row in the table in the database conn with the given
	id. Returns its url value if it is present, returns False otherwise."""
	query = 'select * from %s where id=%d' % (table, id)
	result = conn.execute(query).fetchall()
	if not result: #id not in our database, return False
		return False
	else:
		return str(result[0][1]) #return the url of the id
		
def insert_url(url, table, conn):
	"""Inserts the url into the table in the database conn and returns the id
	of the row which was created by the insert.
	"""
	query = 'insert into %s values(NULL, "%s")' % (table, url)
	c = conn.cursor() #create cursor for this statement so we can get lastrowid
	c.execute(query)
	conn.commit()
	id = c.lastrowid #autoincremented id of the just inserted row
	c.close() #close this cursor, no longer needed
	return id
		
