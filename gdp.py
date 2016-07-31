import csv
import sqlite3 as lite

with open('/home/dssquared/PycharmProjects/Training/UN/Metadata_Indicator_API_NY.GDP.MKTP.CD_DS2_en_csv_v2.csv', 'rU') as inputFile:
    next(inputFile)  # skip the first two lines
    next(inputFile)
    header = next(inputFile)
    inputReader = csv.reader(inputFile)

    con = lite.connect('education.db')
    cur = con.cursor()

    for line in inputReader:
        with con:
            cur.executescript('DROP TABLE IF EXISTS gdp')
            cur.execute('CREATE TABLE gdp'
                        '(')
            cur.execute('INSERT INTO gdp (country_name, _1999, _2000, _2001, _2002, _2003, _2004, _2005, _2006, _2007,'
                        ' _2008, _2009, _2010) VALUES ("' + line[0] + '","' + '","'.join(line[42:-5]) + '");')

