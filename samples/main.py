import dearpygui.dearpygui as dpg
from tradelab.price_iterator import PriceIterator
from utils.data_import import import_data
import time

class ChartsApp:
    def __init__(self, data):
        self.price_iterator = PriceIterator(data)
        self.timeframes = list(data.keys())
        self.create_context()

    def create_context(self):
        dpg.create_context()
        self.create_menus()
        dpg.enable_docking(dock_space=True)

        dpg.configure_app(init_file="dpg.ini")

        self.create_chart_window(None, None, '5min')
        self.create_chart_window(None, None, '1min')
        
        self.create_controls_window()
        

    def create_menus(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="save workspace", callback=self.save_workspace)
            with dpg.menu(label="New_Chart"):
                for timeframe in self.timeframes:
                    dpg.add_menu_item(label=timeframe, callback=self.create_chart_window, user_data=timeframe)
            with dpg.menu(label="Backtest"):
                dpg.add_radio_button(("None", "strat_1", "strat_2"), callback=self.run_backtest, horizontal=False)

    def create_controls_window(self):
        with dpg.window(label="Controls", no_close=True, collapsed=True):
            dpg.add_text("This window has no close button.")

    def create_chart_window(self, sender, app_data, timeframe):
        with dpg.window(label=timeframe):
            
            with dpg.menu_bar():
                with dpg.menu(label="Indicators"):
                    dpg.add_checkbox(label="checkbox", callback=self._indicator)

            with dpg.plot(height=-1, width=-1) as self.main:
                dpg.add_plot_legend()

                # X and Y axes
                self.candle_series_xaxis = dpg.add_plot_axis(dpg.mvXAxis, time=True, no_tick_marks=False, no_tick_labels=False)
                with dpg.plot_axis(dpg.mvYAxis, label="USD") as self.candle_series_yaxis:
                    # Add the candlestick series
                    self.candle_series = dpg.add_candle_series(
                        [int(time.mktime(dt.timetuple())) for dt in self.price_iterator.data[timeframe]['DateTime']],
                        self.price_iterator.data[timeframe]["Open"].tolist(),
                        self.price_iterator.data[timeframe]["Close"].tolist(),
                        self.price_iterator.data[timeframe]["Low"].tolist(),
                        self.price_iterator.data[timeframe]["High"].tolist(),
                        time_unit=dpg.mvTimeUnit_S,
                        parent=self.candle_series_yaxis
                    )


    def run_backtest(self, sender, app_data):
        # Implement backtest logic here
        print("Backtest running for strategy:", app_data)

    def _indicator(self, sender, app_data):
        print(app_data)

    def save_workspace(self):
        dpg.save_init_file("dpg.ini")

    def run(self):
        dpg.create_viewport(title='TradeLab_Charts', width=600, height=200)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

# Run the app
if __name__ == "__main__":

    # Market configuration
    market_config = {
        'date_range': ('2024-05-09', '2024-05-09'),
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


