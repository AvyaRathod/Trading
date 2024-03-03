import angel_one_api_connect as api

dh = api.DataHandling()
dh.Login()
dh.initializeTokenMap()

stocks = [
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
    "HDFC",
    "INFY",
    "ITC",
    "TCS",
    "LT",
    "AXISBANK",
    "KOTAKBANK",
    "HUL",
    "SBI",
    "BAJAJFINSV",
    "ASIANPAINT",
    "MARUTI",
    "M&M",
    "TITAN",
    "HCLTECH",
    "SUNPHARMA",
    "TATAMOTORS",
    "ULTRACEMCO",
    "TATASTEEL",
    "IDFCFIRSTB",
    "POWERGRID",
    "NTPC",
    "BAJAJFINS",
    "NESTLEIND",
    "JSWSTL",
    "TECHM",
    "ADANIENT",
    "HDFCLIFE",
    "GRASIM",
    "DRREDDY",
    "ONGC",
    "HINDALCO",
    "BRITANNIA",
    "SBIN",
    "VIPIND",
    "ADANPORTS",
    "CIPLA",
    "BAJAJAUTO",
    "APOLLOHOSP",
    "TATACONSUM",
    "EICHERMOT",
    "COALINDIA",
    "DIVISLAB",
    "HEROMOTOCO",
    "UPL",
    "BPCL"
]

import time
start_time = time.time()
data_df = dh.dataDownloader(stocks, "2020-12-06 00:00", "2021-12-06 15:00")
end_time = time.time()
print(data_df)

data_df.to_csv("/Users/avyarathod/Desktop/trading/test.csv")
print("\n\n Total Time: {0}".format(end_time-start_time))
