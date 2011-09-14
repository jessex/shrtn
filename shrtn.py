import database as db
import sys, re
from urlparse import urlparse

ALPHABET = "abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789" #no oO0lI1
OURDOMAIN = "http://shr.tn/" #our imaginary domain for our imaginary site
re_short = re.compile(OURDOMAIN + "[a-kmnp-zA-HJ-NP-Z2-9]+$") #matches our URLs
re_end = re.compile("[.][^/]+$") #for checking the end of a url

# ****************************** HELPER FUNCTIONS ******************************

def setup_db():
    """Establishes a connection to our database and creates our url table if it
    does not yet exist. Returns the connection to the database file."""
    conn = db.setup_sql(db.MYLOCATION)
    if conn == None: #Could not establish connection, so quit
        sys.exit()
    if not db.table_exists(db.MYTABLE, conn): #create table if not yet created
        db.create_table(db.MYTABLE, conn)
    return conn

def is_valid_short(url):
    """Takes in a url and determines if it is a valid shortened url."""
    return not (not re_short.match(url))
    
def standardize_url(url):
    """Takes in a url and returns a clean, consistent format. For example:
    example.com, http://example.com, example.com/ all are http://example.com/
    Returns None if the url is somehow invalid."""
    if is_valid_short(url): #will not shorten one of our already shortened URLs
        return None
    parts = urlparse(url, "http") #default scheme is http if omitted
    if parts[0] != "http" and parts[0] != "https": #scheme was not http(s)
        return None
    
    #url appears valid at this point, proceed with standardization
    standard = parts.geturl()
    #work-around for bug in urlparse
    if standard.startswith("http:///") or standard.startswith("https:///"):
        standard = standard.replace("///", "//", 1) #get rid of extra slash
    if not standard.endswith("/"): #does not end with '/'...
        if re_end.findall(standard): #...but ends with .something...
            if parts[0] == "http":
                bound = 7
            elif parts[0] == "https":
                bound = 8
            if standard.rfind("/", bound) == -1: #...and contains no other '/'
                return standard + "/" #append a '/'
    return standard
    
    
# ******************************* CORE FUNCTIONS *******************************

def shorten_url(url, conn):
    """Takes in a standard url and returns a shortened version."""
    url = standardize_url(url)
    if url is None: #tried to shorten invalid url
        return None
    
    #get the id for this url (whether new or otherwise)
    id = db.search_url(url, db.MYTABLE, conn)
    if not id: #url not yet inserted into database
        id = db.insert_url(url, db.MYTABLE, conn) #insert and get its id
    
    code = convert_to_code(id)
    return "%s%s" % (OURDOMAIN, code)
    
def lengthen_url(url, conn):
    """Takes in one of our shortened URLs and returns the correct long url."""
    #isolate code from shortened url
    if not is_valid_short(url): #url was not constructed properly
        return "%s404" % OURDOMAIN
    code = url[14:] #just the code, ie. h7K9g0
    
    id = resolve_to_id(code) #convert shortened code to id
    long = db.search_id(id, db.MYTABLE, conn)
    if not long: #id was not found in database
        return "%s404" % OURDOMAIN #issue 404
    return long #url to perform 301 re-direct on
    
def convert_to_code(id, alphabet=ALPHABET):
    """Converts a decimal id number into a shortened URL code. Use the id of the
    row in the database with the entered long URL."""
    if id <= 0: #invalid codes (autoincrement is always 1 or higher)
        return alphabet[0]
    
    base = len(alphabet) #base to convert to (56 for our standard alphabet)
    chars = []
    while id:
        chars.append(alphabet[id % base])
        id //= base
    chars.reverse() #moved right to left, so reverse order
    return ''.join(chars) #convert stored characters to single string
    
def resolve_to_id(code, alphabet=ALPHABET):
    """Converts the shortened URL code back to an id number in decimal form. Use
    the id to query the database and lookup the long URL."""
    base = len(alphabet)
    size = len(code)
    id = 0
    for i in range(0, size): #convert from higher base back to decimal
        id += alphabet.index(code[i]) * (base ** (size-i-1))
    return id
