from SmartApi import SmartConnect
import requests
import datetime

import pandas as pd

import pyotp
import time

def time_delay(time_delay_val):
    time_start_val = time.time()
    while(time.time() - time_start_val < time_delay_val):
        pass

"""Login"""

class login:
    def __init__(self):
        self.__client_id = "A50876433"
        self.__pwd = "1406"
        self.__api = "mSYvrNuR"
        self.__token = "Z2D573OIJ2PDHCKD66NMIRVGWY"
        self.obj = None

    def Login(self):
        '''logs into angel one'''
        try:

            self.obj = SmartConnect(api_key=self.__api)
            data = self.obj.generateSession(self.__client_id, self.__pwd, pyotp.TOTP(self.__token).now())
            self.refreshToken = data['data']['refreshToken']
            self.feedToken = self.obj.getfeedToken()
            self.userProfile = self.obj.getProfile(self.refreshToken)
            print(self.userProfile)
        except Exception as e:
            print("Login failed: {}".format(e))


class DataHandling(login):
    def __init__(self):
        super().__init__()

    def initializeTokenMap(self):
        '''gets the token map for all tradeables'''

        url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
        d = requests.get(url).json()
        token_df = pd.DataFrame.from_dict(d)
        token_df['expiry'] = pd.to_datetime(token_df['expiry'])
        token_df = token_df.astype({'strike': float})
        self.token_map = token_df
        print(token_df)

    def getTokenInfo(self, symbol, exch_seg='NSE'):
        '''eq_df contains all the details about tradeable eq'''
        df = self.token_map
        if exch_seg == "NSE":
            eq_df = df[(df['exch_seg'] == "NSE") & (df['symbol'].str.contains('EQ'))]
            return eq_df[eq_df['name'] == symbol]

    def OHLCHistory(self, symbol, token, interval, fdate, todate, exchange="NSE"):
        '''
    gets the candle data for one symbol by doing a single api call
  
    task: 
    -make this function such that we can get data more than the limit of the 
    api(ie 30 days for 1 min data)
    -need to get data for n tickers
    '''
        # try:
        historicParam = {
            "exchange": exchange,
            "tradingsymbol": symbol,
            "symboltoken": token,
            "interval": interval,
            "fromdate": fdate,
            "todate": todate
        }

        # the obj in the line below has to be accessed which aint happening
        history = self.obj.getCandleData(historicParam)['data']
        history = pd.DataFrame(history)
        history['ticker'] = symbol

        history = history.reset_index()
        history = history.rename(
            columns={0: "Datetime", 1: "open", 2: "high", 3: "low", 4: "close", 5: "volume"}
        )

        history['Datetime'] = pd.to_datetime(history['Datetime'])
        # history['Datetime'].dt.tz_convert(none)

        self.history = history
        return self.history
        # except Exception as e:
        # print("Historic Api failed: {}".format(e))

    def dataDownloader(self, stocks, start_date, end_date):
        dh = DataHandling
        data_df = pd.DataFrame()
        start_date_final = start_date
        end_date_final = end_date

        stocks = list(stocks)
        
        ErrorCounter = 0
        Didnotworkfuckingidiots = []
        
        for ticker in stocks:
            tokendetails = dh.getTokenInfo(self, ticker).iloc[0]
            symbol = tokendetails['symbol']
            token = tokendetails['token']

            exit = 0

            start_time = datetime.datetime.strptime(start_date_final, '%Y-%m-%d %H:%M')
            start_time += datetime.timedelta(days=-1)
            end_time = start_time + datetime.timedelta(days=1)
            end_date = datetime.datetime.strptime(end_date_final, '%Y-%m-%d %H:%M')

            while exit == 0:

                try:
                    if isinstance(start_time, str):
                        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
                    if isinstance(end_time, str):
                        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')

                    start_time += datetime.timedelta(days=1)
                    end_time += datetime.timedelta(days=1)

                    start_time = start_time.strftime('%Y-%m-%d %H:%M')
                    end_time = end_time.strftime('%Y-%m-%d %H:%M')
                    temp_df = pd.DataFrame()
                    temp_df = dh.OHLCHistory(self, str(symbol), str(token), "ONE_MINUTE", start_time, end_time)
                    
                    print("Date Worked: {0}\t{1}".format(start_time, end_time))
                    data_df = pd.concat([data_df, temp_df], axis=0)

                    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')
                    if end_time > end_date:
                        exit = 1
                    
                    time_delay(0.01)
                    ErrorCounter = 0
                    
                except Exception as err:
                    
                    if(type(err).__name__ == "KeyError"):
                        continue
                    print(f"Unexpected {err=}, {type(err)=}")
                    ErrorCounter+=1
                    if(ErrorCounter >= 10):
                        print("Too many errors Encountered :(")
                        return data_df
                    time_delay(1)
        
        print("Exited While loop")
        print("Stocks that did not work " + str(Didnotworkfuckingidiots))
        return data_df

    def dateTimeCounter(self, data_df):
        temp_df = pd.DataFrame()
        temp_df = data_df
        data_df = temp_df.sort_values(by = ["Datetime", "ticker"], ascending = True)

        # datetimelist = list(data_df['Datetime'])
        dateTimeDictionary = dict(zip(data_df['Datetime'], range(len(data_df['Datetime']))))

        for row in data_df.index():
            key = row.iloc[1]
            data_df['dateTimeCounter'] = dateTimeDictionary[key]

        return data_df
