from tradelab.price_iterator import PriceIterator
from tradelab.indicator_manager import IndicatorManager
from tradelab.broker import Broker
from utils.data_import import import_data


class BackTester:
    def __init__(self, strategy, market_config=None, price_iterator=None, indicators=None):
        if price_iterator is None:
            if market_config is None:
                raise ValueError("Either market_config or price_iterator must be provided")
            date_bounds = market_config['date_range']
            time_bounds = market_config['time_range']
            market = market_config['market']
            timeframes = market_config['timeframes']
            data = import_data(date_bounds, time_bounds, market, timeframes)
            price_iterator = PriceIterator(data)
        
        self.back_test = _BackTester(price_iterator, strategy, indicators)
    
    def run(self):
        self.back_test.run()
        self.create_trades_attribute()

    def create_trades_attribute(self):
        self.trades = self.back_test.broker.closed_trades

class _BackTester:
    def __init__(self, price_iterator, broker, strategy, indicator_manager=None, windows = None):
        self.price_iterator = price_iterator
        self.broker = broker
        self.strategy = strategy
        if indicator_manager != None:
            self.indicator_manager = indicator_manager
        else:
            self.indicator_manager = IndicatorManager(self.price_iterator)
        self.windows = windows
        for indicator_dic in self.strategy.indicators:
            self.indicator_manager.create_indicator(indicator_dic[0], indicator_dic[1])
        self.indicators = self.indicator_manager.active_indicators
        self.resolutions = list(self.price_iterator.data.keys())
        
        if self.windows:
            for window in self.windows.values():
                window.update_candle_serie_plots()
                window.update_current_time_vline()
                window.update_indicator_plots()
       
        self.strategy.next()
        self.broker.update()
        self.next()
        

    def instantiate_indicators(self, indicators):
        self.indicators = {}
        for indicator_class, *params in indicators:
            if params:
                kwargs = params[0]
                instance = indicator_class(self.price_iterator, **kwargs)
            else:
                instance = indicator_class(self.price_iterator)

            self.indicators[indicator_class.__name__] = instance

    def next(self):
        if self.price_iterator.increment != self.strategy.current_increment:
            old_length = self.price_iterator.current_indices[self.resolutions[0]]
            self.price_iterator.change_increment(self.strategy.current_increment)
            new_length = self.price_iterator.current_indices[self.resolutions[0]]
            if old_length != new_length:
                self.indicator_manager.update_active_indicators()
                self.strategy.next()
                self.broker.update()
        else:
            self.price_iterator.next()
            self.indicator_manager.update_active_indicators()
            self.strategy.next()
            self.broker.update()
        
        if self.windows:
            for window in self.windows.values():
                window.update_candle_serie_plots()
                window.update_current_time_vline()
                window.update_indicator_plots()

    def run(self):
        while self.price_iterator.is_next():
            self.next()
            print(self.price_iterator.current_indices[self.price_iterator.resolutions[0]]/len(self.price_iterator.data[self.price_iterator.resolutions[0]]))

    