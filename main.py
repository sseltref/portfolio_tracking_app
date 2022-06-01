import kivy
kivy.require('2.0.0')
import datetime
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from kivy.uix.image import Image
import sqlite3
from sqlite3 import Error
import time
from kivy.config import Config

class Button(Button):
    pass


class Main(TabbedPanel):
    pass


class MyApp(App):
    def update_chart(self, x=''):
        self.apka.ids._chart_img.reload()
        self.apka.ids._chart_img2.reload()
        self.apka.ids.labelval.text = str(x)
    def update_chart2(self):
        self.apka.ids._chart_img2.reload()




    @staticmethod
    def create_connection(db):
        conn = None

        try:
            conn = sqlite3.connect(db)
        except Error as e:
            print(e)

        return conn

    def date_to_epoch(self, year, month, day):
        date = datetime.datetime(int(year),int(month), int(day))
        date = date.timestamp()

        return date


    def make_transaction(self, conn, tr_date, currency1, currency2, volume):
        cur = conn.cursor()
        cur.execute('INSERT INTO history(tr_date, currency1, currency2, volume) VALUES (?, ?, ?, ?)',
                    (tr_date, currency1, currency2, float(volume)))
        conn.commit()

    ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
                  VALUES(?,?,?,?,?,?) '''

    conn_tr = create_connection('Database/database.db')

    @staticmethod
    def rename_asset(ticker):
        if ticker == 'USD':
            return 'USD'
        elif ticker == 'BTC':
            return 'BTC-USD'
        else:
            return f'{ticker}=X'


    def stock_data(self, ticker, period, interval, observation):
        plt.clf()

        ticker = yf.Ticker(MyApp.rename_asset(ticker))

        ticker_history = ticker.history(period, interval)

        sf = ticker_history[observation]
        df = pd.DataFrame({'Date': sf.index, 'Values': sf.values})

        x = df['Date'].tolist()
        y = df['Values'].tolist()

        plt.style.use('dark_background')
        plt.plot(x, y)
        plt.ylabel('Price($)')
        plt.xlabel('Date', rotation=0)
        plt.savefig('foo.png')


    def historical_value(self, ticker,conn=conn_tr):
        if ticker != all:
            values = {}
            cur = conn.cursor()
            v = 0

            cur.execute(f"SELECT * FROM history WHERE currency1='{ticker}' OR currency2='{ticker}'")
            # print(cur.fetchall())
            operations = sorted(cur.fetchall(), key=lambda x: x[1])
            for line in operations:
                if line[3] == ticker:
                    v -= float(line[4])
                else:
                    v += float(line[4])

                values[int(line[1])] = round(v, 2)
            x = list(values.keys())
            y = list(values.values())
            for i in range(len(x)):
                x[i] = datetime.datetime.fromtimestamp(x[i])
        else:
            values, v = {}, 0

            cur = conn.cursor()

            cur.execute(f"SELECT * FROM history")
            operations = sorted(cur.fetchall(), key=lambda x: x[1])

            conn.close()

            # print(ticker)

            for line in operations:
                date = datetime.datetime.fromtimestamp(line[1]).strftime('%Y-%m-%d')
                # print(line)
                'sell part'
                try:
                    if line[2] == 'USD':
                        outcome = float(line[4])
                    else:
                        x = yf.download(ticker[line[2]], date, date)
                        outcome = x['Close'].tolist()[0] * float(line[4])
                    # print(outcome)

                    y = yf.download(ticker[line[3]], date, date)
                    income = y['Close'].tolist()[0] * float(line[4])

                    v += round(income - outcome, 2)
                    values[line[1]] = v

                except:
                    continue

            x = list(values.keys())
            y = list(values.values())
            for i in range(len(x)):
                x[i] = datetime.datetime.fromtimestamp(x[i])
        plt.clf()
        plt.style.use('dark_background')
        plt.plot(x, y)
        plt.ylabel('Value')
        plt.xlabel('Date', rotation=0)
        plt.savefig('foo2.png')
    @staticmethod
    def value(ticker=None, conn = conn_tr):
        values = {}
        cur = conn.cursor()

        cur.execute("SELECT * FROM history")

        for line in cur.fetchall():
            c1, c2, v = line[2], line[3], float(line[4])

            if c1 not in values:
                values[c1] = 0
            else:
                values[c1] += v

            if c2 not in values:
                values[c2] = 0
            else:
                values[c2] -= v

            for line in values:
                values[line] = round(values[line], 2)

        if ticker == None:
            return values
        else:
            return values[ticker]


    # returns dictionary with historical values (key: data) of one ticker (given in parameter)
    @staticmethod
    def import_tickers(conn = conn_tr):
        ticker = {}
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM tickers")

        for line in cur.fetchall():
            ticker[line[0]] = line[1]

        return ticker
    @staticmethod
    def current_portfolio_value(ticker=import_tickers(), values=value()):
        v = 0
        for line in values:
            if line == 'USD':
                v += values[line]
            else:
                stock = yf.Ticker(ticker[line])
                price = stock.info['regularMarketPrice']
                v += price * values[line]

        # print(line, values[line], v)
        return round(v, 2)

    # returns current value of portfolio (in USD)
    # returns historical value ins USD of all assets in portfolio as a dictionary (key - date in epoch)
    @staticmethod
    def assets_to_sell(conn=conn_tr):
        export = []
        cur = conn.cursor()

        cur.execute("SELECT DISTINCT currency2 FROM history")

        for line in cur.fetchall():
            export.append(line[0])
        return export

    @staticmethod
    def stock_historical(values, date):
        try:
            price = values.loc[date.strftime("%Y-%m-%d")]['Close']
        except:
            return MyApp.stock_historical(values, date + datetime.timedelta(-1))
        else:
            return price



    @staticmethod
    def portfolio_values(conn = conn_tr, ticker = import_tickers()):
        values, v = {}, 0
        all_tickers_history = {}
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM history")
        operations = sorted(cur.fetchall(), key=lambda x: x[1])

        # print(ticker)

        for line in operations:
            date = datetime.datetime.fromtimestamp(line[1])
            if ticker[line[2]] not in all_tickers_history:
                yo = yf.Ticker(ticker[line[2]]).history(period='max')
                all_tickers_history[ticker[line[2]]] = yo

            if ticker[line[3]] not in all_tickers_history:
                yo = yf.Ticker(ticker[line[3]]).history(period='max')
                all_tickers_history[ticker[line[3]]] = yo

            sell = MyApp.stock_historical(all_tickers_history[ticker[line[2]]], date)
            buy = MyApp.stock_historical(all_tickers_history[ticker[line[3]]], date)


            v += buy * float(line[4]) - sell * float(line[4])
            values[line[1]] = v

        # print(line[1], v)

        # print(date, ticker[line[2]], ticker[line[3]], line)
        # print(values[line[1]], v)

        x = list(values.keys())
        y = list(values.values())
        for i in range(len(x)):
            x[i] = datetime.datetime.fromtimestamp(x[i])
        plt.clf()
        plt.style.use('dark_background')
        plt.plot(x, y)
        plt.ylabel('Value')
        plt.xlabel('Date', rotation=0)
        plt.savefig('foo2.png')

    # returns historical value ins USD of all assets in portfolio as a dictionary (key - date in epoch)
    assets_held = assets_to_sell()
    def build(self):
        plt.savefig('foo.png')
        plt.savefig('foo2.png')
        self.apka = Main()
        return  self.apka

if __name__ == '__main__':
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '800')
    MyApp().run()

