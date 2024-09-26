import dearpygui.dearpygui as dpg
import time
from tradelab.price_iterator import PriceIterator
from utils.data_import import import_data

# Market configuration
market_config = {
    'date_range': ('2024-01-09', '2024-05-09'),
    'time_range': ('14:00:00', '17:00:00'),
    'market': 'wallstreet',
    'timeframes': ['1sec', '5min']
}

# Load market data
date_bounds = market_config['date_range']
time_bounds = market_config['time_range']
market = market_config['market']
timeframes = market_config['timeframes']
data = import_data(date_bounds, time_bounds, market, timeframes)

price_iterator = PriceIterator(data)

class DummyChart:
    def __init__(self, data):
        self.price_iterator = PriceIterator(data)
        self.ohlc = price_iterator.simulation_data['1sec']
        self.symbol = "dax"  # Your stock symbol
        
        # Initialize GUI components
        self._setup_ui()

    def _setup_ui(self):
        """Sets up the UI components including the candlestick chart."""
        with dpg.window(label="Candlestick Chart"):
            with dpg.plot(label="Candlestick Chart", height=400, width=-1) as self.main:
                dpg.add_plot_legend()

                # X and Y axes
                self.candle_series_xaxis = dpg.add_plot_axis(dpg.mvXAxis, time=True, no_tick_marks=False, no_tick_labels=False)
                with dpg.plot_axis(dpg.mvYAxis, label="USD") as self.candle_series_yaxis:
                    # Add the candlestick series
                    self.candle_series = dpg.add_candle_series(
                        [int(time.mktime(dt.timetuple())) for dt in self.ohlc['DateTime']],
                        self.ohlc["Open"].tolist(),
                        self.ohlc["Close"].tolist(),
                        self.ohlc["Low"].tolist(),
                        self.ohlc["High"].tolist(),
                        time_unit=dpg.mvTimeUnit_S,
                        label=self.symbol,
                        parent=self.candle_series_yaxis
                    )
                # with dpg.add_drawlist()

                times = [int(time.mktime(dt.timetuple())) for dt in self.ohlc['DateTime']]
                self.a = dpg.draw_line((times[0], 18550), (times[10], 18550), color=(255, 0, 0, 255), thickness=1)
                
                    # self.candle_series = dpg.add_candle_series(
                    #     self.ohlc.index.to_list(),
                    #     self.ohlc["Open"].tolist(),
                    #     self.ohlc["Close"].tolist(),
                    #     self.ohlc["Low"].tolist(),
                    #     self.ohlc["High"].tolist(),
                    #     time_unit=dpg.mvTimeUnit_S,
                    #     label=self.symbol,
                    #     parent=candle_series_xaxis
                    # )
              
    

        # Show the viewport
        dpg.create_viewport(title='Candlestick Chart Example', width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        # Simulate the listener in a background thread
        dpg.set_frame_callback(1, self.dummy_listener)

    def dummy_listener(self):
        """Simulates a listener that updates the chart every second with new data."""
        while True:
            
            print("Updating chart with new data...")

            time.sleep(0.005)
            
            price_iterator.next()
            self.ohlc = price_iterator.simulation_data['1sec']

            # Update the candlestick chart with new data
            dpg.configure_item(
                self.candle_series,
                dates=[int(time.mktime(dt.timetuple())) for dt in self.ohlc['DateTime']],
                opens=self.ohlc["Open"].tolist(),
                highs=self.ohlc["High"].tolist(),
                lows=self.ohlc["Low"].tolist(),
                closes=self.ohlc["Close"].tolist()
            )
            
            
            times = [int(time.mktime(dt.timetuple())) for dt in self.ohlc['DateTime']]
            if self.a:
                self.a = dpg.delete_item(self.a)
                print(self.a)
            else:
                self.a = dpg.draw_line((times[0], 18550), (times[10], 18550), color=(255, 0, 0, 255), thickness=1, parent=self.main)
            # dpg.configure_item(
            #     self.a,
            #     p1 = (times[1], 18550)
            # )

            

            # dpg.configure_item(
            #             self.candle_series,
            #             dates = self.ohlc.index.to_list(),
            #             opens = self.ohlc["Open"].tolist(),
            #             closes = self.ohlc["Close"].tolist(),
            #             lows = self.ohlc["Low"].tolist(),
            #             highs = self.ohlc["High"].tolist()
            #         )


            # Fit axis data after updating the chart
            # dpg.fit_axis_data(dpg.get_item_parent(self.candle_series))

if __name__ == "__main__":
    dpg.create_context()
    chart = DummyChart(data)

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
