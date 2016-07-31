"""
Thinkful.com Training
Unit3 - UN Education Data Scraping

Use code below to scan through the table contents to find starting points:
for index, row in enumerate(soup(<index string>)):
    print(<index string>, index)
    print(row)
"""

from bs4 import BeautifulSoup
import requests
import sqlite3 as lite
import csv
import pandas as pd
import numpy as np

# URL for the UN data set
url = "https://raw.githubusercontent.com/dsunwoo/UN/master/Scrape.html"

r = requests.get(url)
soup = BeautifulSoup(r.content)

# Working table - Using above code, table index 11 is the starting point of the data
main_table = soup('table')[11]
header_row = main_table('tr')[7]

# Scrape the data from table
data_list = []
for x in range(8, 191):
    data_row = main_table('tr')[x]
    data = []
    for cell in data_row('td'):
        data.append(cell.get_text())
    # Create a list of values for datatable
    data_list.append([data[0], int(data[1]), int(data[4]), int(data[7]), int(data[10])])

# Connect and setup database
con = lite.connect('education.db')
cur = con.cursor()
with con:
    # Check for existing tables and remove
    cur.executescript('DROP TABLE IF EXISTS school_life')
    cur.executescript('DROP TABLE IF EXISTS gdp')
    cur.executescript('DROP TABLE IF EXISTS school_gdp')
    # Initiate the School life expectancy table
    cur.execute('CREATE TABLE school_life '
                '(Country TEXT, '
                'Year INT, '
                'Total INT, '
                'Men INT, '
                'Women INT);'
                )
    # Initiate the GDP table
    cur.execute('CREATE TABLE gdp'
                '(country_name TEXT,'
                '_1999 REAL, _2000 REAL, _2001 REAL, _2002 REAL,'
                '_2003 REAL, _2004 REAL, _2005 REAL, _2006 REAL,'
                '_2007 REAL, _2008 REAL, _2009 REAL, _2010 REAL);'
                )
    # Initiate the master table for School life and GDP Joined
    cur.execute('CREATE TABLE school_gdp (Country TEXT, Year INT, Total_Years INT, GDP REAL);')

# populate tables
with con:
    cur.executemany('INSERT INTO school_life VALUES (?,?,?,?,?)', data_list)  # School Life Expectancy

with open('/home/dssquared/PycharmProjects/Training/UN/API_NY.GDP.MKTP.CD_DS2_en_csv_v2.csv', 'rU') as inputFile:
    next(inputFile)  # skip the first 4 lines
    next(inputFile)
    next(inputFile)
    next(inputFile)
    header = next(inputFile)
    inputReader = csv.reader(inputFile)
    for line in inputReader:
        with con:
            cur.execute('INSERT INTO gdp '
                        '(country_name, _1999, _2000, _2001, _2002, '
                        '_2003, _2004, _2005, _2006, _2007, _2008, _2009, _2010) '
                        'VALUES ("' + line[0] + '","' + '","'.join(line[43:55]) + '");')
con.close()

"""
# place table into a dataframe
df = pd.read_sql_query("SELECT * FROM school_life", con, index_col="Country")

# Basic stats
men_mean = df['Men'].mean()
men_median = df['Men'].median()
women_mean = df['Women'].mean()
women_median = df['Women'].median()
print("\nSchool Life Expectancy Statistics:\n")
print("Men - Mean = {}    Median = {}".format(str(round(men_mean, 2)), str(men_median)))
print("Women - Mean = {}    Median = {}\n".format(str(round(women_mean, 2)), str(women_median)))
"""
