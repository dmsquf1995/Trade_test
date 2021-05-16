from re import T
import time
import pyupbit
import datetime
import numpy as np

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time
    
def get_current_price(ticker) :
    """ 현재가 조회 """
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def get_open_price(ticker) :
    """ 시가 조회 """
    df = pyupbit.get_ohlcv(ticker, count=1)
    return df.iloc[0]['open']

def get_high_price(ticker) :
    """ 고가 조회 """
    df = pyupbit.get_ohlcv(ticker, count=1)
    return df.iloc[0]['high']

def get_target_price(ticker, k) :
    """ 매수 목표가 조회 """
    df = pyupbit.get_ohlcv(ticker, count=1)
    return df.iloc[0]['open'] * k # 시가의 -k %

'''
전일대비 -k % 이상인 코인에 대한 매수, p % 수익, 하루에 한 번 매수
'''

coin_name = pyupbit.get_tickers(fiat="KRW")

ch = 0 # 판매 상태 확인 0 : 코인 찾는 중 1 : 코인 매수 함 2 : 코인 매도 함
buy_coin = None
p = 1.02 # 수익률
k = 0.97 # 시가의 -5 %
money = 10000

while False : # 9시까지 거래 금지
    now = datetime.datetime.now()
    start_time = get_start_time("KRW-BTC")
    end_time = start_time + datetime.timedelta(days=1)

    if now >= end_time - datetime.timedelta(minutes=2) :
        break
    print("아직 9시가 아닙니다")

    time.sleep(60)
    
print("AUTOTRADE START",money)

# 자동매매 시작
while True :
    try :

        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if buy_coin == None : # 코인을 사지 않았을 때

            if start_time < now < end_time - datetime.timedelta(minutes=2) :
                
                for coin in coin_name : # 현재 사기 가장 좋은 코인 고르기

                    target_price = get_target_price(coin, k) # 목표 가격
                    current_price = get_current_price(coin) # 현재 가격

                    print(format(coin, " >10s"), "   현재가 : %11.2f"%current_price, "   목표가 : %11.2f"%target_price)
                    
                    if target_price >= current_price and ch == 0 :
                        
                        if money > 5000 :
                            
                            buy_coin = coin # 매수 코인의 이름
                            buy_coin_price = get_current_price(coin) # 매수 코인의 가격
                            coin_count = money / buy_coin_price
                            money = money - (buy_coin_price * coin_count)
                            ch = 1
                            break

        else : # 코인을 샀을 때
            
            print(buy_coin, "   현재가 :", get_current_price(buy_coin), "   매수가 : ",buy_coin_price, "    목표 수익가 : ",buy_coin_price*p)

            if start_time < now < end_time - datetime.timedelta(minutes=2) :

                if ch == 1 :

                    if buy_coin_price * p <= get_current_price(buy_coin) : # p % 이상 오르면 매도

                        if coin_count * get_current_price(buy_coin) > 5000 :
                            
                            money = coin_count * get_current_price(buy_coin)
                            coin_count = 0
                            buy_coin = None
                            ch = 2
                            print(money)

            else :

                if ch == 1 :

                    if coin_count * get_current_price(buy_coin) > 5000 :

                            money = coin_count * get_current_price(buy_coin)
                            coin_count = 0
                            print(money)

                buy_coin = None
                ch = 0

        #time.sleep(0.01)

    except Exception as e :
        print(e)
        #time.sleep(0.01)