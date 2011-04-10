# shrtn: a simple URL shortening engine

## Description

shrtn is a project to satisfy a personal curiosity: learning what's under the 
hood of URL shortening services. The best way to learn (for some of us) is to 
actually do, so I decided to write a URL shortening engine in my favorite 
language, without actually intending to place it online because there is such 
a glut of URL shorteners on the web that it hardly seems worth it.

shrtn accepts a URL, standardizes it to a cleaner and more consistent format if 
necessary, inserts it into an sqlite database and uses the autoincrementing row 
id of that insert to generate a code. This code is found by doing a simple base 
conversion based on the amount of characters eligible for our shortened URL 
codes. The output is the handy, convenient, (and hopefully shiny) new short URL!

## Instructions

shrtn.py contains the core logic of the actual shortening engine while the 
database.py file contains the functions necessary for interacting with an 
sqlite database. Included in the repository is a testrig.py file which contains 
some basic unit tests of the engine. To examine how this implementation of URL 
shortening works, run the test rig and of course examine the thoroughly 
commented code for yourself. 

To run the test rig, place the source files into a directory and, inside of 
said directory, create a folder with the same name as the prefix of the 
LOCATION variable in database.py file. On line 3 of database.py, it reads:

    LOCATION = "shrtn/db" #location of database file

So inside of the directory with the source files, create a folder named "shrtn" 
so that an sqlite database file named "db" will have a location for storage. 
Then simply run

    $ python testrig.py

to quickly run the testing script.

## Deficiencies

The database can only accept up to 9,223,372,036,854,775,808 unique URLs due to 
the fact that the largest possible integer key is 9,223,372,036,854,775,807. 
However, this seems to be big enough. :)

With regards to the "URL standardization," more work can be done. At present, 
it accepts URLs as obviously invalid as "a/bc". The methodology is to take in a 
URL, check that it is not one of our shortened URLs, check that its scheme is 
either HTTP or HTTPS and then run it into the urlparse module in Python. This 
is then re-extracted and a "/" is placed at the end of the path if deemed 
necessary, so that a URL like example.com will become http://example.com/. 
As already mentioned, some obviously invalid URLs will be allowed. Also, this 
draws a distinction between www.example.com and example.com which for some 
URLs might be unwanted. 

I attempted to use John Gruber's URL validation regex at 
<a href="http://daringfireball.net/2009/11/liberal_regex_for_matching_urls">Daring Fireball. 
However, it turned away some URLs for me which I would prefer included and I did 
not feel like messing with it too much. I may revisit this in the future.

## License

Copyright (c) 2011 Joshua Essex

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    
