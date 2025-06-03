# 載入必要套件
import requests,datetime,os,time
import numpy as np
import matplotlib.dates as mdates
#from talib.abstract import *  # 載入技術指標函數

    
class KBar:
    def __init__(self, start_date, cycle_duration):
        self.Cycle = cycle_duration  # 單位為分鐘
        self.TAKBar = {
            'time': [],
            'open': [],
            'high': [],
            'low': [],
            'close': [],
            'volume': []
        }
        self.last_bar_time = None

    def AddPrice(self, time, open_price, close_price, low_price, high_price, qty):
        if not self.TAKBar['time']:
            # 第一根K棒，初始化
            self.TAKBar['time'].append(time)
            self.TAKBar['open'].append(open_price)
            self.TAKBar['high'].append(high_price)
            self.TAKBar['low'].append(low_price)
            self.TAKBar['close'].append(close_price)
            self.TAKBar['volume'].append(qty)
            self.last_bar_time = time
            return 1  # 新增K棒

        # 若未設 last_bar_time，則視為初始化
        if self.last_bar_time is None:
            self.last_bar_time = time

        # 計算時間差（分鐘）
        delta_minute = (time - self.last_bar_time).total_seconds() / 60

        if delta_minute >= self.Cycle:
            # 超過週期：新增新K棒
            self.TAKBar['time'].append(time)
            self.TAKBar['open'].append(open_price)
            self.TAKBar['high'].append(high_price)
            self.TAKBar['low'].append(low_price)
            self.TAKBar['close'].append(close_price)
            self.TAKBar['volume'].append(qty)
            self.last_bar_time = time
            return 1
        else:
            # 更新當前K棒（最後一筆）
            idx = -1
            self.TAKBar['high'][idx] = max(self.TAKBar['high'][idx], high_price)
            self.TAKBar['low'][idx] = min(self.TAKBar['low'][idx], low_price)
            self.TAKBar['close'][idx] = close_price
            self.TAKBar['volume'][idx] += qty
            return 0



            
