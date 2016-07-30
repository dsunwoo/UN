from bs4 import BeautifulSoup
import requests
import sqlite3 as lite
import pandas as pd
import numpy as np

# URL for the UN data set
url = "https://raw.githubusercontent.com/dsunwoo/UN/master/Scrape.html"

r = requests.get(url)
soup = BeautifulSoup(r.content)

# Use code below to scan through the table contents to find starting points
"""
for index, row in enumerate(soup(<index string>)):
    print(<index string>, index)
    print(row)
"""
# Working table - Using above code, table index 11 is the starting point of the data
main_table = soup('table')[11]
header_row = main_table('tr')[7]

# Setting up dictionaries
d_year = {}
d_total = {}
d_men = {}
d_women = {}

# Scrape the data from table
country_list = []
for x in range(8, 191):
    data_row = main_table('tr')[x]
    data = []
    for cell in data_row('td'):
        data.append(cell.get_text())
    # Populate dictionaries with appropriate cell values
    country_list.append(data[0])
    d_year[data[0]] = data[1]
    d_total[data[0]] = data[4]
    d_men[data[0]] = data[7]
    d_women[data[0]] = data[10]

# Setup database
col_names = ('Country', 'Year', 'Discard1', 'Discard2', 'Total', 'Men', 'Women')
con = lite.connect('education.db')
cur = con.cursor()
with con:
    cur.executescript('DROP TABLE IF EXISTS school_life')
    cur.execute('CREATE TABLE school_life '
                '(Country STRING, '
                'Year INT, '
                'Discard1 STRING, '
                'Discard2 STRING, '
                'Total INT, '
                'Men INT, '
                'Women INT);'
                )
# Create an empty dataset


con.close

