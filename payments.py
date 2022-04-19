import configparser
import datetime
from flask import Flask
import json
import pandas as pd
import time
import requests


app = Flask(__name__)

class Miner:

    def __init__(self, name, wallet):
        self.name = name
        self.wallet = wallet

    def get_weekly_payments(self):
        res = requests.get(f"https://gpumine.org/api/bill?currency=ETH&address={self.wallet}").text
        payments = json.loads(res)['data']['payments']
        lastWeek  = datetime.datetime.today() - datetime.timedelta(weeks=1)

        payment = {}
        for p in payments:
            paidDate = datetime.datetime.fromisoformat(p['date'][:10])
            if paidDate > lastWeek:
                payment[str(paidDate)[:10]] = p['paid']
            else:
                break
        
        return payment


def get_miner_dataframe():
    minerList = configparser.ConfigParser()
    minerList.read('miner.ini')
    df = pd.DataFrame()
    for name, address in (dict(minerList)['miner']).items():
        print(f'Get {name}....')

        m = Miner(name, address)
        payment = m.get_weekly_payments()
        df = df.append(pd.Series(payment, name = name))
        time.sleep(3)

    df = df.reindex(sorted(df.columns), axis=1)
    df['sum'] = df.sum(axis=1)

    return df


@app.route('/')
def index():
    return MINER_DATA.to_html()


if __name__ == '__main__':
    MINER_DATA = get_miner_dataframe()
    app.run('0.0.0.0', debug=False, port=8888)