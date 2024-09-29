import dearpygui.dearpygui as dpg
from tradelab.price_iterator import PriceIterator
from utils.data_import import import_data
import time
import numpy as np


class ChartsApp:
    def __init__(self, data):
        self.price_iterator = PriceIterator(data)
        self.timeframes = list(data.keys())
        self.create_context()
        self.window_counter = 0
        self.tags = {}
        self.backtest_switch = False

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
                for timeframe in self.timeframes:
                    dpg.add_menu_item(label=timeframe, callback=self.create_chart_window, user_data=timeframe)
            with dpg.menu(label="Backtest"):
                dpg.add_radio_button(("None", "strat_1", "strat_2"), callback=self.backtest_switch, horizontal=False)

    def create_controls_window(self):
        with dpg.window(label="Controls", no_close=True, collapsed=True):
            dpg.add_text("This window has no close button.")
            dpg.add_radio_button(self.timeframes, default_value=None, callback=self.change_increment)
            dpg.add_button(label="Next_iteration", callback=self.next_iteration)

    def create_chart_window(self, sender, app_data, timeframe):
        window_tag = f'window_{self.window_counter}'
        plot_tag = f'plot_{self.window_counter}'
        x_axis_tag = f'x-axis_{self.window_counter}'
        y_axis_tag = f'y-axis_{self.window_counter}'
        candel_series = f'candel_series_{self.window_counter}'
        
        with dpg.window(label=timeframe, width=400, height=400, tag=window_tag):
            with dpg.menu(label="Indicators"):
                dpg.add_checkbox(label="checkbox", callback=self._indicator, user_data=[timeframe,y_axis_tag])
                dpg.add_checkbox(label="e", callback=self._indicator)
        dpg.add_plot(height=-1, width=-1, parent=window_tag, tag=plot_tag)
        dpg.add_plot_legend(parent=plot_tag) 
        dpg.add_plot_axis(dpg.mvXAxis, time=False, no_tick_marks=False, parent=plot_tag,no_tick_labels=False, tag=x_axis_tag)
        dpg.add_plot_axis(dpg.mvYAxis, label="USD",parent=plot_tag, tag=y_axis_tag)
        dpg.add_candle_series(self.price_iterator.simulation_data[timeframe].index.tolist(),
                            self.price_iterator.simulation_data[timeframe]["Open"].tolist(),
                            self.price_iterator.simulation_data[timeframe]["Close"].tolist(),
                            self.price_iterator.simulation_data[timeframe]["Low"].tolist(),
                            self.price_iterator.simulation_data[timeframe]["High"].tolist(),
                            time_unit=dpg.mvTimeUnit_S,
                            parent=y_axis_tag,
                            tag = candel_series)
        
        self.window_counter +=1

    def update_candel_series(self):
        
        dpg.configure_item(
            self.candle_series,
            dates=self.ohlcv["dates"].tolist(),
            opens=self.ohlcv["opens"].tolist(),
            highs=self.ohlcv["highs"].tolist(),
            lows=self.ohlcv["lows"].tolist(),
            closes=self.ohlcv["closes"].tolist(),
        )

    def next_iteration(self):
        self.price_iterator.next()
        self.update_candel_series()

    def change_increment(self, sender, timeframe):
        previous_time = self.price_iterator.current_time
        self.price_iterator.change_increment(timeframe)
        new_time = self.price_iterator.current_time
        if previous_time != new_time:
            #update candelsticks 
            ...
    def backtest_switch(self, sender, app_data):
        ...

    def run_backtest(self, switch):
        # Implement backtest logic here
        print("Backtest running for strategy:", switch)

    def _indicator(self, sender, app_data, timeframe):
        print(sender, app_data, timeframe)
        # print(timeframe[1])

        # constant_list = [39000 for _ in range(len(self.price_iterator.data[timeframe[0]].index.tolist()))]
        # dpg.add_line_series(self.price_iterator.data[timeframe[0]].index.tolist(), constant_list, label="0.5 + 0.5 * sin(x)", parent=timeframe[1])
        

        

    def save_workspace(self):
        dpg.save_init_file("dpg.ini")

    def run(self):
        dpg.create_viewport(title='TradeLab_Charts', width=600, height=200)
        dpg.setup_dearpygui()
        dpg.show_viewport()       
        while dpg.is_dearpygui_running():
            self.run_backtest(self.backtest_switch)
            dpg.render_dearpygui_frame()

        dpg.start_dearpygui()
        dpg.destroy_context()

# Run the app
if __name__ == "__main__":

    # Market configuration
    market_config = {
        'date_range': ('2024-04-09', '2024-05-09'),
        'time_range': ('14:00:00', '17:00:00'),
        'market': 'wallstreet',
        'timeframes': ['1sec','1min', '5min']
    }

    # Load market data
    date_bounds = market_config['date_range']
    time_bounds = market_config['time_range']
    market = market_config['market']
    timeframes = market_config['timeframes']
    data = import_data(date_bounds, time_bounds, market, timeframes)
    
    app = ChartsApp(data)
    app.run()


