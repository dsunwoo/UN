from bs4 import BeautifulSoup
import requests

# URL for the UN data set
url = "https://raw.githubusercontent.com/dsunwoo/UN/master/Scrape.html"

r = requests.get(url)
soup = BeautifulSoup(r.content)

# Initial table
for index, row in enumerate(soup('table')):
    print('table', index)
    print(row)

# Working table
main_table = soup('table')[11]
# Find data in each row
for index, row in enumerate(main_table('tr')):
    if row.get_text().find("Country or area") != -1 and row.get_text().find("Year") != -1 and row.get_text().find("Total") != -1:
        print('tr', index)
        print(row.get_text())

print(main_table('tr')[8])
