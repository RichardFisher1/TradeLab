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
        self.start_switch = False

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
                dpg.add_radio_button(("None", "strat_1", "strat_2"), tag='backtest', callback=self._backtest_switch, horizontal=False)

    def create_controls_window(self):
        with dpg.window(label="Controls", no_close=True, collapsed=True):
            dpg.add_text("This window has no close button.")
            dpg.add_radio_button(self.timeframes, default_value=None, callback=self.change_increment)
            dpg.add_button(label="Next_iteration", callback=self.next_iteration)
            dpg.add_button(label="Start", callback=self.start)
            dpg.add_button(label="Stop", callback=self.stop)

    def create_chart_window(self, sender, app_data, timeframe):
        window_tag = f'window_{self.window_counter}'
        plot_tag = f'plot_{self.window_counter}'
        x_axis_tag = f'x-axis_{self.window_counter}'
        y_axis_tag = f'y-axis_{self.window_counter}'
        candle_series_tag = f'candle_series_{self.window_counter}'
        view_format = 'Daily View'
        
        self.tags[window_tag] = {'plot': plot_tag, 
                                 'timeframe': timeframe,
                                 'view' : view_format,
                                 'x_axis': x_axis_tag,
                                 'y_axis': y_axis_tag,
                                 'candle_series': candle_series_tag}

        with dpg.window(label=timeframe, width=400, height=400, tag=window_tag):
            with dpg.menu_bar():
                with dpg.menu(label="Indicators"):
                    dpg.add_checkbox(label="checkbox", callback=self._indicator, user_data=self.tags[window_tag])
                    dpg.add_checkbox(label="e", callback=self._indicator)
                with dpg.menu(label="Veiw"):
                    dpg.add_radio_button(("Free View", "Daily View", "Custom View2"), default_value='Daily View', callback=self._veiw, user_data=self.tags[window_tag])
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
                            tag = candle_series_tag)
        
        self.update_axis_limits(self.tags[window_tag])
        self.window_counter +=1
    
    def update_axis_limits(self, window_tags):
        x_axis_tag = window_tags['x_axis']
        y_axis_tag = window_tags['y_axis'] 
        view = window_tags['view']
        timeframe = window_tags['timeframe']
        
        if view == 'Free View':
            pass
        elif view == 'Daily View':
            xmin, xmax, ymin, ymax = v1(self.price_iterator, timeframe)
            dpg.set_axis_limits(x_axis_tag, xmin, xmax)
            dpg.set_axis_limits(y_axis_tag, ymin, ymax)
        




    def update_candel_series(self):        
        for _, window_items in self.tags.items():
            timeframe = window_items['timeframe']
            candle_series = window_items['candle_series']
            dpg.configure_item(
                candle_series,
                dates=self.price_iterator.simulation_data[timeframe].index.tolist(),
                opens=self.price_iterator.simulation_data[timeframe]["Open"].tolist(),
                highs=self.price_iterator.simulation_data[timeframe]["High"].tolist(),
                lows=self.price_iterator.simulation_data[timeframe]["Low"].tolist(),
                closes=self.price_iterator.simulation_data[timeframe]["Close"].tolist(),
            )

    def next_iteration(self):
        self.price_iterator.next()
        self.update_candel_series()

    def start(self):
        self.start_switch = True
    
    def stop(self):
        self.start_switch = False

    def change_increment(self, sender, timeframe):
        previous_time = self.price_iterator.current_time
        self.price_iterator.change_increment(timeframe)
        new_time = self.price_iterator.current_time
        if previous_time != new_time:
            #update candelsticks 
            ...
    
    def _veiw(self, sender, app_data, user_data):
        print(app_data, user_data)
    
    def _backtest_switch(self, sender, app_data):
        if app_data == 'None':
            self.backtest_switch = False
        else:
            self.backtest_switch = True

    def run_backtest(self, switch):
        ...

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

            if self.start_switch is True:
                self.next_iteration()
            
            for _, window_tags in self.tags.items():
                self.update_axis_limits(window_tags)
            
            
            dpg.render_dearpygui_frame()

        dpg.start_dearpygui()
        dpg.destroy_context()


def v1(price_iterator, timeframe):
    n_bars_in_day = price_iterator.n_bars_in_day[timeframe]
    open_of_day_index = price_iterator.current_indices[timeframe] // (n_bars_in_day) * n_bars_in_day
    open_of_day = price_iterator.simulation_data[timeframe].iloc[open_of_day_index, 1]
    xmin = open_of_day_index - 0.5
    xmax = open_of_day_index - 0.5 + n_bars_in_day
    ymax = max(open_of_day + 50, max(price_iterator.simulation_data[timeframe].iloc[open_of_day_index:open_of_day_index+n_bars_in_day, 2])) + 5
    ymin = min(open_of_day - 50, min(price_iterator.simulation_data[timeframe].iloc[open_of_day_index:open_of_day_index+n_bars_in_day, 3])) - 5
    return xmin, xmax, ymin, ymax


# Run the app
if __name__ == "__main__":

    # Market configuration
    market_config = {
        'date_range': ('2024-04-19', '2024-05-09'),
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


