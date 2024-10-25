import pandas as pd
import numpy as np

class ValueBasedIndicators:
    def __init__(self, data_iterator, timeframe, period, column_names):
        self.data_iterator = data_iterator
        self.current_update_index = self.data_iterator.current_indices[timeframe]
        self.period = period
        self.timeframe = timeframe
        self.column_names = column_names
        self.initialize_data()

    def initialize_data(self):
        self.data = pd.DataFrame(columns=['DateTime'] + self.column_names)
        self.data['DateTime'] = self.data_iterator.data[self.timeframe]['DateTime'].copy()
        price_data = self.data_iterator.data[self.timeframe].copy()
        result = price_data.groupby(price_data['DateTime'].dt.date).apply(self.indicator).reset_index(level=0, drop=True)    
        print('hello>', result)    
        self.data[self.column_names] = result.reset_index(level=0, drop=True)

        self.update()

    def update(self, change_increment = False):
        if change_increment == False:
            self.current_update_index = self.data_iterator.current_indices[self.timeframe]
            if self.current_update_index >= self.period:
                price_data = self.data_iterator.simulation_data[self.timeframe].iloc[self.current_update_index-self.period:self.current_update_index+1, :].copy()
                
                print('1', price_data.groupby(price_data['DateTime'].dt.date).apply(self.indicator))
                result = price_data.groupby(price_data['DateTime'].dt.date).apply(self.indicator).reset_index(level=0, drop=True) 
                
                print('3',result)
                
                
                self.data.loc[self.current_update_index, self.column_names] = result.loc[self.current_update_index, self.column_names]
            

        if change_increment == True:
            if self.current_update_index >= self.period:
                price_data = self.data_iterator.simulation_data[self.timeframe].iloc[self.current_update_index-self.period:self.current_update_index+1, :].copy()
                result = price_data.groupby(price_data['DateTime'].dt.date).apply(self.indicator).reset_index(level=0, drop=True) 
                self.data.loc[self.current_update_index, self.column_names] = result.loc[self.current_update_index, self.column_names]
                self.current_update_index = self.data_iterator.current_indices[self.timeframe]
                price_data = self.data_iterator.simulation_data[self.timeframe].iloc[self.current_update_index-self.period:self.current_update_index+1, :].copy()
                result = price_data.groupby(price_data['DateTime'].dt.date).apply(self.indicator).reset_index(level=0, drop=True) 
                self.data.loc[self.current_update_index, self.column_names] = result.loc[self.current_update_index, self.column_names]

            # self.test = pd.DataFrame(columns=['DateTime'] + self.column_names)
            # self.test['DateTime'] = self.data_iterator.simulation_data[self.timeframe]['DateTime'].copy()
            # price_data = self.data_iterator.simulation_data[self.timeframe].copy()
            # result = price_data.groupby(price_data['DateTime'].dt.date).apply(self.indicator).reset_index(level=0, drop=True)        
            # self.test[self.column_names] = result.reset_index(level=0, drop=True)
            # print(self.data.iloc[:current_index,:].equals(self.test.iloc[:current_index,:]))






















        # for index in valid_indicator_indice:
        #         values = 
        #         for col_idx in range(len(values)):
        #             self.data.iloc[index, col_idx + 1] = values[col_idx]
        

       
  # valid_indicator_indice = []
        # total_rows = len(self.data)
        # block_size = self.data_iterator.n_bars_in_day[self.timeframe]
        # for i in range(0, total_rows, block_size):
        #     block_range = list(range(i, i + block_size))
        #     valid_indicator_indice += block_range[self.period:] 
  

    # def update_indicators(self):
        
    #         for index in self.indicators_indices_to_update():
    #             values = self.update()
    #             for col_idx in range(len(values)):
    #                 self.data[tf].iloc[index, col_idx + 1] = values[col_idx]

















    # def indicators_indices_to_update(self):
    #     for tf in self.timeframes:   
    #         latest_updated_indicator_index = self.data[tf].iloc[:, 1:].last_valid_index()
    #         if latest_updated_indicator_index is not None:
    #             missing_indices = list(np.arange(latest_updated_indicator_index+1, self.data_iterator.current_indices[tf] + 1))
    #         else:
    #             missing_indices = list(np.arange(0, self.data_iterator.current_indices[tf] + 1))
            
    #         if not missing_indices:
    #             missing_indices.append(self.data_iterator.current_indices[tf])
    #         elif missing_indices[-1] != self.data_iterator.current_indices[tf]:
    #             missing_indices.append(self.data_iterator.current_indices[tf])
            
    #         missing_indices_copy = missing_indices.copy()
    #         idx = 0
    #         while idx < len(missing_indices_copy):
    #             index = missing_indices_copy[idx]
    #             # Remove index if day's data has less than required period
    #             if index in range(self.data_iterator.n_bar_in_day[tf] * (index // self.data_iterator.n_bar_in_day[tf]), self.data_iterator.n_bar_in_day[tf] * (index // self.data_iterator.n_bar_in_day[tf]) + self.period):
    #                 missing_indices.remove(index)
    #             idx += 1  # Otherwise, increment index normally
    #         return missing_indices
        
    # def update_indicators(self):
    #     for tf in self.timeframes:
    #         for index in self.indicators_indices_to_update():
    #             values = self.update()
    #             for col_idx in range(len(values)):
    #                 self.data[tf].iloc[index, col_idx + 1] = values[col_idx]
            
    def indicator(self):
        raise NotImplementedError("Subclasses should implement this!")
    
    def open(self, tf, index):
        flipped_data = self.data_iterator.simulation_data[tf].iloc[:self.data_iterator.current_indices[tf]+1].reset_index(drop=True)
        flipped_data = flipped_data.iloc[::-1].reset_index(drop=True)
        return flipped_data.loc[index, 'Close'] 
    
    def close(self, tf, index):
        flipped_data = self.data_iterator.data[tf].iloc[:self.data_iterator.current_indices[tf]+1].reset_index(drop=True)
        flipped_data = flipped_data.iloc[::-1].reset_index(drop=True)
        return flipped_data.loc[index, 'Close'] 
    
    def high(self, tf, index):
        flipped_data = self.data_iterator.simulation_data[tf].iloc[:self.data_iterator.current_indices[tf]+1].reset_index(drop=True)
        flipped_data = flipped_data.iloc[::-1].reset_index(drop=True)
        return flipped_data.loc[index, 'High'] 
    
    def low(self, tf, index):
        flipped_data = self.data_iterator.simulation_data[tf].iloc[:self.data_iterator.current_indices[tf]+1].reset_index(drop=True)
        flipped_data = flipped_data.iloc[::-1].reset_index(drop=True)
        return flipped_data.loc[index, 'Low'] 



# class FunctionBasedIndicators:
#     def __init__(self, data_iterator):
#         self.data_iterator = data_iterator
#         self.period = None
#         self.timeframes = []
#         self.column_names = None

#     def initialize_df(self):
#         self.data = {}
#         for tf in self.timeframes:
#             df = pd.DataFrame(columns=['DateTime'] + self.column_names)
#             df['DateTime'] = self.data_iterator.simulation_data[tf]['DateTime'].copy()
#             self.data[tf] = df

#     def indicators_indices_to_update(self):
#         for tf in self.timeframes:   
#             latest_updated_indicator_index = self.data[tf].iloc[:, 1:].last_valid_index()
#             if latest_updated_indicator_index is not None:
#                 missing_indices = list(np.arange(latest_updated_indicator_index+1, self.data_iterator.current_indices[tf] + 1))
#             else:
#                 missing_indices = list(np.arange(0, self.data_iterator.current_indices[tf] + 1))
            
#             if not missing_indices:
#                 missing_indices.append(self.data_iterator.current_indices[tf])
#             elif missing_indices[-1] != self.data_iterator.current_indices[tf]:
#                 missing_indices.append(self.data_iterator.current_indices[tf])
            
#             missing_indices_copy = missing_indices.copy()
#             idx = 0
#             while idx < len(missing_indices_copy):
#                 index = missing_indices_copy[idx]
#                 # Remove index if day's data has less than required period
#                 if index in range(self.data_iterator.n_bar_in_day[tf] * (index // self.data_iterator.n_bar_in_day[tf]), self.data_iterator.n_bar_in_day[tf] * (index // self.data_iterator.n_bar_in_day[tf]) + self.period):
#                     missing_indices.remove(index)
#                 idx += 1  # Otherwise, increment index normally
#             return missing_indices
        
#     def update_indicators(self):
#         for tf in self.timeframes:
#             for index in self.indicators_indices_to_update():
#                 values = self.update()
#                 for col_idx in range(len(values)):
#                     self.data[tf].iloc[index, col_idx + 1] = values[col_idx]
            
#     def update(self):
#         raise NotImplementedError("Subclasses should implement this!")
    
#     def function(self):
#         raise NotImplementedError("Subclasses should implement this!")
    
#     def open(self, tf, index):
#         flipped_data = self.data_iterator.simulation_data[tf].iloc[:self.data_iterator.current_indices[tf]+1].reset_index(drop=True)
#         flipped_data = flipped_data.iloc[::-1].reset_index(drop=True)
#         return flipped_data.loc[index, 'Open'] 
    
#     def close(self, tf, index):
#         flipped_data = self.data_iterator.simulation_data[tf].iloc[:self.data_iterator.current_indices[tf]+1].reset_index(drop=True)
#         flipped_data = flipped_data.iloc[::-1].reset_index(drop=True)
#         return flipped_data.loc[index, 'Close'] 
    
#     def high(self, tf, index):
#         flipped_data = self.data_iterator.simulation_data[tf].iloc[:self.data_iterator.current_indices[tf]+1].reset_index(drop=True)
#         flipped_data = flipped_data.iloc[::-1].reset_index(drop=True)
#         return flipped_data.loc[index, 'High'] 
    
#     def low(self, tf, index):
#         flipped_data = self.data_iterator.simulation_data[tf].iloc[:self.data_iterator.current_indices[tf]+1].reset_index(drop=True)
#         flipped_data = flipped_data.iloc[::-1].reset_index(drop=True)
#         return flipped_data.loc[index, 'Low'] 
    
    

 