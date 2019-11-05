from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

urlpage = 'https://ca.finance.yahoo.com/quote/CBA.AX/history?period1=686127600&period2=1414479600&interval=1d&filter=history&frequency=1d'
request = Request(urlpage)
webpage = urlopen(request).read()
soup = BeautifulSoup(webpage, 'html5lib')

table = soup.find('table', attrs={'data-test':'historical-prices'})
foot = table.tfoot
body = table.tbody

data_html = body.select('tr')

for i in np.arange(0,100):
    tag = data_html[i]
    datum = tag.find_all('td')
    print(datum[0])

body = pd.DataFrame(body)
body.to_csv('test')    