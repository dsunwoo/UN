from bs4 import BeautifulSoup
import requests

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
# Scrape the header list
header_cols = []
data = {}
for cell in header_row('td'):
    header_cols.append(cell.get_text())
# Replace the empty column names with NA
# [('NA' if v is "" else v is v) for v in header_cols]
# Scrape the data from table
for col_name in header_cols:
    for x in range(8, 190):
        data_row = main_table('tr')[x]
        for cell in data_row('td'):
            data[col_name] = (cell.get_text())
"""
for row in main_table('tr'):
    if row.get_text().find("Country or area") != -1 \
            and row.get_text().find("Year") != -1 \
            and row.get_text().find("Total") != -1:
        print('tr', index)
        print(row)
"""