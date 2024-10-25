from tradelab.indicator import ValueBasedIndicators
import pandas as pd
import pandas_ta as ta
import numpy as np

class mav(ValueBasedIndicators):
    def __init__(self, data_iterator, timeframe):
        super().__init__(data_iterator, timeframe, period=0, column_names=['mav'])
    
    def indicator(self, data):
        mav = (data['Close'].shift(0))
        return pd.DataFrame({'mav': mav})
        
class channel(ValueBasedIndicators):
    def __init__(self, data_iterator, timeframe):
        super().__init__(data_iterator, timeframe, period=3, column_names=['upper', 'lower'])
            
    def indicator(self, data):
        upper = data['Open'].shift(1).rolling(window=3).mean()
        lower = data['Close'].shift(1).rolling(window=3).mean()
        return pd.DataFrame({'upper': upper, 'lower': lower})

class atr(ValueBasedIndicators):
    def __init__(self, data_iterator, timeframe, period=3):
        super().__init__(data_iterator, timeframe, period=period, column_names=['atr'])
        self.period = period
    
    def indicator(self, data):
        atr_values = ta.atr(high=data['High'], low=data['Low'], close=data['Close'], length=self.period)
        if atr_values is None or len(atr_values) == 0:
            atr_df = pd.DataFrame({'atr': np.nan}, index=data.index)        
        else:
            atr_df = pd.DataFrame({'atr': atr_values}, index=data.index)
        return atr_df




























class my_ind_1(ValueBasedIndicators):
    def __init__(self, data_iterator, **kwargs):
        super().__init__(data_iterator)
        self.period = 0
        self.timeframes = ['5min']
        self.column_names = ['Lower_bound', 'Upper_bound']
        self.initialize_df()

        self.param1 = kwargs.get('param1', 1)
        self.param2 = kwargs.get('param2', 1)

    def update(self):
        lower_bound = self.low('5min', 0)
        upper_bound = self.high('5min', 0)     
        return lower_bound, upper_bound
    
# class my_ind_5(FunctionBasedIndicators):
#     def __init__(self, data_iterator):
#         super().__init__(data_iterator)
#         self.period = 2
#         self.timeframes = ['5min']
#         self.column_names = ['a', 'b', 'c']
#         self.x_0 = 'current_bar'
#         self.x_veiw = [-2,-1,0,1]
#         self.initialize_df()

#     def update(self):
#         x = [-2,-1,0]
#         y = [(self.low('5min', 2)+self.high('5min', 2))/2,
#             (self.low('5min', 1)+self.high('5min', 1))/2, 
#             (self.low('5min', 0)+self.high('5min', 0))/2]
#         self.coefficients = np.polyfit(x, y, 2)
#         a = self.coefficients[0]
#         b = self.coefficients[1]
#         c = self.coefficients[2]
#         return a, b, c
    
#     def function(self, coefficients):
#         return np.poly1d(coefficients)
    
















    
       
         