import argparse
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


parser = argparse.ArgumentParser(description='Filter coins by daily change')
parser.add_argument('climit', help='Select 24hour change bounds', type=float)
args = parser.parse_args()


def parse_table(climit):
    
    try:
        req = requests.get('https://coinmarketcap.com/all/views/all/')
    except Exception as exc:
        print('Connection Error')
        
    soup = BeautifulSoup(req.content, 'lxml')
    MAXLIM = 1000
    
    coins = [i.text for i in soup.find_all('a', class_='currency-name-container')][:MAXLIM]
    prices = [re.sub(r'[$,]', '', i.text) for i in soup.find_all('a', class_='price')][:MAXLIM]
    volumes = [re.sub(r'[$,]', '', i.text) for i in soup.find_all('a', class_='volume')][:MAXLIM]
    day_changes = [float(i.text.replace('%', '')) for i in soup.find_all(attrs={'data-timespan': '24h'})][:MAXLIM]
       
    try:
        data = {'Name': coins, 'Price': prices, 'Volume': volumes, 'Change': day_changes}
        df = pd.DataFrame(data, columns=['Name', 'Price', 'Volume', 'Change'])
        if not day_changes:
            print('No Results')
    except Exception as exc:
        print(exc)

    res = df[(df.Change <= climit) & (df.Change >= -climit)]

    print(f'Found {len(res)} Results: \n\n', res.to_string())


if __name__ == '__main__':
    parse_table(args.climit)











    
