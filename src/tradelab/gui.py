import json
import os
import dearpygui.dearpygui as dpg
from tradelab.price_iterator import PriceIterator
from tradelab.indicator_manager import IndicatorManager
from tradelab.strategy_manager import StrategyManager
from tradelab.backtester import _BackTester
from tradelab.broker import Broker
from utils.helper_functions import get_class_names_from_file
from tradelab.window import Window
import pandas as pd
import time
from datetime import datetime, timedelta




class ChartsApp:
    def __init__(self, data):
        self.current_time = datetime.now()
        self.speed = timedelta(seconds=0)

        self.window_counter = 0
        self.windows = {}
        self.window_configs = []
        
        self.price_iterator = PriceIterator(data)
        self.broker = Broker(self.price_iterator)
        self.indicator_manager = IndicatorManager(self.price_iterator)
        self.strategy_manager = StrategyManager(self.price_iterator, self.broker)
        
        self.backtest_switch = False
        self.start_switch = False
        self.print_switch = False
        self.closed_trades_window_open = False
        self.equity_curve_window_open = False
        
        self.previous_data = pd.DataFrame()
        self.current_data = pd.DataFrame()

        self.create_context()
        self.load_worksape()
      
    ### ---------- CREATE GUI COMPONENTS - MENUS & WINDOWS ---------- ###

    def create_context(self):
        dpg.create_context()
        self.create_menus()
        self.create_controls_window()
        dpg.configure_app(docking=True, docking_space=True, init_file="dpg.ini", load_init_file=True)
        
    def create_menus(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="save workspace", callback=self.save_workspace)
            with dpg.menu(label="New_Chart"):
                for timeframe in self.price_iterator.data.keys():
                    dpg.add_menu_item(label=timeframe, callback=self.create_chart_window, user_data=timeframe)
            with dpg.menu(label="Visual_Backtest"):
                dpg.add_radio_button(("None", "strat_1", "strat_2"), tag='backtest', callback=self._backtest_switch, horizontal=False)
            with dpg.menu(label="Closed_Trades"):
                dpg.add_checkbox(
                    label='Closed Trades', 
                    callback=self.toggle_closed_trades_window,
                    tag = 'closed_trades_checkbox_tag'
                )
            with dpg.menu(label="Equity_Curve"):  # New menu for equity curve
                dpg.add_checkbox(
                    label='Cumulative Profit', 
                    callback=self.toggle_equity_curve_window,
                    tag='equity_curve_checkbox_tag'
                )

            dpg.add_separator() 
            dpg.add_text(f"Time: {self.price_iterator.current_time}", tag="current_time_text")
    
    def _print_switch(self, sender, app_data):
            self.print_switch = app_data
    
    def print(self):
        self.current_data = self.backtest.broker.closed_trades
        self.current_data['cumulative_profit'] = self.current_data['profit'].cumsum()
        if not self.previous_data.equals(self.current_data): 
            self.previous_data = self.current_data
            print(self.current_data)

    def create_controls_window(self):
        with dpg.window(label="Controls", no_close=True, collapsed=True):
            dpg.add_slider_float(label="Speed", default_value=0.5, max_value=1, min_value=0, callback=self.update_speed)
            dpg.add_radio_button(list(self.price_iterator.data.keys()), default_value=None, callback=self.change_increment)
            dpg.add_button(label="Next_iteration", callback=self.next_iteration)
            dpg.add_button(label="Start", callback=self.start)
            dpg.add_button(label="Stop", callback=self.stop)
            dpg.add_button(label="Next_day", callback=self.next_day)
    
    def toggle_equity_curve_window(self, sender, app_data):
        if app_data:  # Checkbox checked
            self.open_equity_curve_window()
        else:  # Checkbox unchecked
            self.close_equity_curve_window()

    def open_equity_curve_window(self):
        if not self.equity_curve_window_open:
            with dpg.window(label="Equity Curve", tag='equity_curve_window_tag', on_close=self.close_equity_curve_window):
                # Create a plot for the equity curve
                with dpg.plot(label="Equity Curve", height=-1, width=-1):
                    dpg.add_plot_legend()
                    self.equity_curve_plot = dpg.add_line_series([], label="Cumulative Profit", tag='equity_curve_series_tag')

            self.equity_curve_window_open = True
            self.update_equity_curve_window()

    def close_equity_curve_window(self):
        if self.equity_curve_window_open:
            dpg.delete_item('equity_curve_window_tag')  # Close the window
            self.equity_curve_window_open = False
        dpg.set_value('equity_curve_checkbox_tag', False)

    def update_equity_curve_window(self):
        if self.broker.closed_trades is not None:
            cumulative_profit = self.broker.closed_trades['profit'].cumsum()  # Calculate cumulative profit
            self.equity_curve_data = cumulative_profit.tolist()  # Convert to list for plotting
            
            # Update the equity curve line series
            if self.equity_curve_window_open and self.equity_curve_plot is not None:
                dpg.set_value('equity_curve_series_tag', self.equity_curve_data)





    def toggle_closed_trades_window(self, sender, app_data):
        if app_data:  # Checkbox checked
            self.open_closed_trades_window()
        else:  # Checkbox unchecked
            self.close_closed_trades_window()

    def open_closed_trades_window(self):
        if not self.closed_trades_window_open:
            with dpg.window(label="Closed Trades", tag='closed_trades_window_tag', on_close=self.close_closed_trades_window):
                self.trades_text = dpg.add_text("")
            self.closed_trades_window_open = True
            self.update_closed_trades_window()

    def close_closed_trades_window(self):
        if self.closed_trades_window_open:
            dpg.delete_item('closed_trades_window_tag')  # Close the window
            self.closed_trades_window_open = False

        dpg.set_value('closed_trades_checkbox_tag', False)

    def update_closed_trades_window(self):
        self.current_data = self.broker.closed_trades
        self.current_data['cumulative_profit'] = self.current_data['profit'].cumsum()
        trades_info = self.current_data.to_string(index=False)
        
        # Update the trades text
        if self.closed_trades_window_open:
            dpg.set_value(self.trades_text, trades_info)




    def create_chart_window(self, sender, app_data, timeframe):
        window_tag = f'window_{self.window_counter}'
        self.windows[window_tag] = Window(self.window_counter, timeframe, self.price_iterator, self.indicator_manager)
        self.window_counter +=1

        self.window_configs.append({'timeframe': timeframe})
  
    def _backtest_switch(self, sender, strategy_name):
        if strategy_name == 'None':
            self.backtest_switch = False
        else:
            self.strategy_manager.activate_strategy(strategy_name)
            strategy = self.strategy_manager.active_strategy[strategy_name]['strategy']
            for indicator_name, timeframe in strategy.indicators:
                self.indicator_manager.create_indicator(indicator_name, timeframe)
            
            self.backtest = _BackTester(self.price_iterator, self.broker, strategy, self.indicator_manager)
            self.backtest_switch = True
    
    def load_worksape(self):
        try:
            with open('config.txt', 'r') as file:
                loaded_config = json.load(file)
        except FileNotFoundError:
            loaded_config = {"windows": []}

        for window in loaded_config['windows']:
            self.create_chart_window(None, None, timeframe=window['timeframe']) 

        dpg.configure_app(init_file="dpg.ini")
    
    def save_workspace(self):
        dpg.save_init_file("dpg.ini")

        config = { 
        'windows': self.window_configs  # Save the timeframes of the created windows 
        }

        with open('config.txt', 'w') as file:
            json.dump(config, file)

    def update_displayed_time(self):
        dpg.set_value("current_time_text", f"Time: {self.price_iterator.current_time}")
    
    def update_speed(self, sender, app_data):
        
        self.speed = timedelta(seconds=app_data * 5)
    ### ---------- CONTROLLER ---------- ###

    def speed_of_simulation(self, delta):
        if datetime.now() > self.current_time + delta:
            self.current_time = datetime.now()  # Update the current time
            return True  # Proceed with iteration
        return False  #
     

    def next_iteration(self):
        if not self.speed_of_simulation(delta=self.speed): 
            return
        self.backtest.next() if self.backtest_switch else self.price_iterator.next()
        self.indicator_manager.update_active_indicators()
        for window in self.windows.values():
                window.update_candle_serie_plots()
                window.update_current_time_vline()
                window.update_indicator_plots()
              
    def change_increment(self, sender, timeframe):
        previous_time = self.price_iterator.current_time
        self.price_iterator.change_increment(timeframe)
        new_time = self.price_iterator.current_time
        self.indicator_manager.update_active_indicators()
        self.indicator_manager.update_active_indicators(change_increment=True)
        if previous_time != new_time:
            for window in self.windows.values():
                window.update_candle_serie_plots()
                window.update_indicator_plots()

    def start(self):
        self.start_switch = True
    
    def stop(self):
        self.start_switch = False

    def next_day(self):
        self.price_iterator.next_day()
        self.indicator_manager.update_active_indicators()
        for window in self.windows.values():
                window.update_candle_serie_plots()
                window.update_indicator_plots()
 
    ### -------- MAIN FLOW ------------------ ###
             
    def run(self):
        dpg.create_viewport(title='TradeLab_Charts', width=600, height=200)
        dpg.setup_dearpygui()
        dpg.show_viewport()       
        while dpg.is_dearpygui_running():
            
            if self.indicator_manager.update_available_indicators():
                 for window in self.windows.values():
                    window.update_indicator_menu()  # right now this updates also active indicators and checked_indicators
                    window.update_indicator_plots()
            
            if self.strategy_manager.update_available_strategies():
                ...

            if self.backtest_switch is True:
                for window in self.windows.values():
                    window.update_candle_serie_plots()
                    window.update_current_time_vline()
                    window.update_indicator_plots()
            
            if self.start_switch is True:
                self.next_iteration()
                if self.print_switch == True:
                    self.print()
            
            self.update_displayed_time()
            
            for window in self.windows.values():
                window.update_axis_limits()


            if self.closed_trades_window_open:
                self.update_closed_trades_window()
            
            if self.equity_curve_window_open:
                self.update_equity_curve_window()
            
            
            

            dpg.render_dearpygui_frame()

            

        dpg.start_dearpygui()
        dpg.destroy_context()

