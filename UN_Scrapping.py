"""
Thinkful.com Training
Unit4 - UN Education Data Scraping

Use code below to scan through the table contents to find starting points:
for index, row in enumerate(soup(<index string>)):
    print(<index string>, index)
    print(row)
"""

from bs4 import BeautifulSoup
import requests
import sqlite3 as lite
import pandas as pd
import numpy as np

# URL for the UN data set
url = "https://raw.githubusercontent.com/dsunwoo/UN/master/Scrape.html"

r = requests.get(url)
soup = BeautifulSoup(r.content)

# Working table - Using above code, table index 11 is the starting point of the data
main_table = soup('table')[11]
header_row = main_table('tr')[7]

# Setting up dictionaries
d_data = {}

# Scrape the data from table
data_list = []
for x in range(8, 191):
    data_row = main_table('tr')[x]
    data = []
    for cell in data_row('td'):
        data.append(cell.get_text())
    # Create a list of values for datatable
    data_list.append([data[0], int(data[1]), int(data[4]), int(data[7]), int(data[10])])

# Setup database
con = lite.connect('education.db')
cur = con.cursor()
with con:
    cur.executescript('DROP TABLE IF EXISTS school_life')
    cur.execute('CREATE TABLE school_life '
                '(Country TEXT, '
                'Year INT, '
                'Total INT, '
                'Men INT, '
                'Women INT);'
                )
# populate database
with con:
    cur.executemany('INSERT INTO school_life VALUES (?,?,?,?,?)', data_list)
con.close

