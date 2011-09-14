from shrtn import *
import database as db


if __name__ == "__main__":
    conn = setup_db() #setup connection to database
    assert db.table_exists(db.MYTABLE, conn) == True #check that table is ready
    
    #unit tests for shrtn functions
    good_short = "http://shr.tn/h7Ki9a"
    bad_short = "http://shr.tn/a8CT/bnb"
    assert is_valid_short(good_short) == True
    assert is_valid_short(bad_short) == False
    
    standard = "http://example.com/"
    assert standardize_url("example.com") == standard
    assert standardize_url("http://example.com") == standard
    assert standardize_url("www.example.com/") != standard #do not adjust www
    
    assert standardize_url(good_short) is None #do not shorten our own URLs
    assert standardize_url("ftp://aserver/afile") is None #only http(s) allowed
    
    id = 78950039
    code = convert_to_code(id)
    a = resolve_to_id(code)
    assert a == id
    print "%d -> %s -> %d" % (id, code, a)
    
    id = -1 #should resolve to 0 so should not equal resolved id
    code = convert_to_code(id)
    assert resolve_to_id(code) != id
    print "%d -> %s -> %d" % (id, code, id)
    
    id = 17180131327 #large prime number
    code = convert_to_code(id)
    assert resolve_to_id(code) == id
    print "%d -> %s -> %d" % (id, code, id)
    
    #unit tests for shortening/lengthening
    shortened = shorten_url("example.com", conn) 
    lengthened = lengthen_url(shortened, conn)
    assert lengthened == standard
    print "%s -> %s -> %s" % ("example.com", shortened, lengthened)
    
    id = db.search_url(standard, db.MYTABLE, conn)
    assert db.search_id(id, db.MYTABLE, conn) == standard
    
    wiki = "http://en.wikipedia.org/wiki/List_of_prime_numbers"
    shortened = shorten_url(wiki, conn)
    lengthened = lengthen_url(shortened, conn)
    assert lengthened == wiki
    print "%s -> %s -> %s" % (wiki, shortened, lengthened)
    
    
    
    
    