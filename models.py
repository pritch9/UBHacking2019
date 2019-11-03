
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import requests
import io
from sklearn.metrics import mean_squared_error as rms
import numpy as np
import math 
import os
import helper
present_dir=os.path.dirname(os.path.abspath(__file__))
path="\data\AMZN.csv"
# XGboost regressor
# Random Forest Regressor
# LSTM
# Conv LSTM

# Interpretebility using lime

class Models(object):
        
    def ret_uni_data(self):        
        plt.figure(num=None, figsize=(20, 2), dpi=100,facecolor='w', edgecolor='k')
        plt.plot(data.index,data["Adj Close"],marker='*', color='maroon')
        plt.show()        

    def uni_baseline(self,data,steps):
        pred_values=[]

        end =steps
        values = data[:-end]
        actual_values = data[len(data)-end:]
        pred_values=[]
        indexes=data[len(data)-end:].index

        for i in range(1,len(actual_values)):
            pred_values.append(actual_values[i])
            
        pred_values.append(0)
        
        """plt.figure(num=None, figsize=(20, 2), dpi=100,facecolor='w', edgecolor='k')
        plt.xlabel('Time', fontsize=8)
        plt.ylabel('Adjusted Stock ', fontsize=8)
        plt.plot(actual_values,marker='.', color='pink')
        plt.plot(pred_values,marker='.', color='purple')
        plt.title("Adjusted Stocks ",fontsize=12)
        plt.show()
        """

        rmse=math.sqrt(rms(actual_values,pred_values))
        print("RMSE VALUE : ",rmse)
        return { "model":"Baseline","index":list(indexes), "actual":list(actual_values.values), "predicted":list(pred_values),"rmse":rmse}
         
    def uni_sarima(self,data,steps):
        return helper.sarima(data,steps)

    def lstm(self,data,steps):
        return helper.lstm(data,steps)

if __name__=="__main__":
    data = pd.read_csv(present_dir+path, error_bad_lines=False,header=0, parse_dates=[1], index_col=0, squeeze=True)
    data["Adj Close"] = data["Adj Close"].astype(float)
    data=data.loc[:,"Adj Close"]
    data=data[:500]
    data=pd.Series(data)

    steps=10
    obj=Models()
    obj.uni_baseline(data,steps)
    #print(obj.uni_sarima(data,steps))
    print(obj.lstm(data,steps))
    

