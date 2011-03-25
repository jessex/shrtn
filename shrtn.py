import database as db
import sys


OURDOMAIN = "http://shr.tn/" #our imaginary domain for our imaginary shortener


def setup_db():
	"""Establishes a connection to our database and creates our url table if it
	does not yet exist. Returns the connection to the database file."""
	conn = db.setup_sql()
	if conn == None: #Could not establish connection, so quit
		sys.exit()
	if not db.table_exists(db.MYTABLE, conn): #create table if not yet created
		db.create_table(db.MYTABLE, conn)
	return conn

def shorten_url(url):
	"""Takes in a standard url and returns a shortened version."""
	
	#get the id for this url (whether new or otherwise)
	id = db.search_url(url, db.MYTABLE, conn)
	if not id: #url not yet inserted into database
		id = db.insert_url(url, db.MYTABLE, conn) #insert and get its id
	

def lengthen_url(short):
	"""Takes in one of our shortened urls and returns its long form."""
	#convert shortened code to id
	
	url = db.search_id(id, db.MYTABLE, conn)
	if not url: #id was not found in database
		return False #you would likely want to 404 here
	return url #url to perform 301 re-direct on
	
def convert_to_code(url):
	pass
	
def resolve_to_url(code):
	pass

