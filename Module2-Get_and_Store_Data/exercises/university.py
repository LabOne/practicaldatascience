import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('universitydb.sqlite')
cur = conn.cursor()

# Create tables in a database
cur.executescript('''
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Course;

CREATE TABLE Student (
    ID         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Name       TEXT UNIQUE
);

CREATE TABLE Course (
    ID         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Title      TEXT UNIQUE,
	StudentID  INTEGER
);

''')


fname = 'University.xml' #Use this file to fill up Tables in our database

#We need to parse the following XML structures:
# <key>MemberID</key><integer>123</integer>
# <key>Name</key><string>John Doe</string>
# <key>Title</key><string>Practical Data Science</string>
def lookup(d, keyName):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == keyName :
            found = True
    return None

stuff = ET.parse(fname) #Parsing of XML file
all_entries = stuff.findall('dict/dict/dict')
print('Dict count:', len(all_entries)) #Total number of entries = number of members of all courses
for entry in all_entries:
    if ( lookup(entry, 'MemberID') is None ) : continue #Sanity check

    title = lookup(entry, 'Title') #Get the title of course
    name = lookup(entry, 'Name') #Get the name of student who attends this course

    if name is None or title is None : #Sanity check
        continue

    print(title, name)

    cur.execute('''INSERT OR IGNORE INTO Student (Name)
        VALUES ( ? )''', ( name, ) ) #( name,) should be a tuple
    cur.execute('SELECT ID FROM Student WHERE Name = ? ', (name, )) #Extract the studentID from database 
    studentID = cur.fetchone()[0] #(we do not know what ID was used for each student)
	
    cur.execute('''INSERT OR IGNORE INTO Course (Title,StudentID) 
        VALUES ( ?,? )''', ( title,studentID  ) ) #Use studentID as a Foreign key in Course Table

conn.commit()