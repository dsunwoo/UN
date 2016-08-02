from bs4 import BeautifulSoup
import requests
import sqlite3 as lite
import pandas as pd
import numpy as np

# Connect and setup database
con = lite.connect('education.db')
cur = con.cursor()

# place gdp table into a dataframe
df = pd.read_sql_query("SELECT * FROM gdp", con)

# gdp_tall = []

"""
for i in range(0, len(df)-1):
    for k,v in df.items():
        if k != 'country_name':
            gdp_tall.append([df['country_name'][i], k, df[k][i]])
"""