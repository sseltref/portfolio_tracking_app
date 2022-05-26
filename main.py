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
    def update_chart(self):
        self.apka.ids._chart_img.reload()


    def reload_chart(self):
        Main

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
                    (tr_date, currency1, currency2, volume))
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

    @staticmethod
    def assets_to_sell(conn=conn_tr):
        export = []
        cur = conn.cursor()

        cur.execute("SELECT DISTINCT currency2 FROM history")

        for line in cur.fetchall():
            export.append(line[0])

        return export

    assets_held = assets_to_sell()
    def build(self):
        plt.savefig('foo.png')
        self.apka = Main()
        return  self.apka

if __name__ == '__main__':
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '800')
    MyApp().run()

