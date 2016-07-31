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
d_data = {}
# d_year = {}
# d_total = {}
# d_men = {}
# d_women = {}

# Scrape the data from table
country_list = []
data_list = []
for x in range(8, 191):
    data_row = main_table('tr')[x]
    data = []
    for cell in data_row('td'):
        data.append(cell.get_text())
    # Populate dictionaries with appropriate cell values
    data_list.append([data[0], int(data[1]), int(data[4]), int(data[7]), int(data[10])])
    # country_list.append(data[0])

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
    # Create an empty dataset
    # for country in range(0, len(country_list)-1):
    #    cur.execute("INSERT INTO school_life(Country) VALUES (?)", (country_list[country],))
# Insert data into table
    cur.executemany('INSERT INTO school_life VALUES (?,?,?,?,?)', data_list)

    # for x in range(0, len(data_list)-1):
    #    cur.execute('UPDATE school_life SET Country = ' + data_list[x][0] +
    #                ', Year = ' + data_list[x][1] +
    #                ', Total = ' + data_list[x][4] +
    #                ', Men = ' + data_list[x][7] +
    #                ', Women = ' + data_list[x][10])
con.close

