from tradelab.strategy import Strategy
from my_indicators import mav

class strat_1(Strategy):
    def __init__(self, data_iterator, broker, indicator_manager, indicators = [('mav', '5min')]):
        super().__init__(data_iterator, broker, indicator_manager)
        self.indicators = indicators
        self.CumulateOrders = False
        self.TradeIntraday = True
        self.step = 0
        self.data_iterator.change_increment('5min')
        self.data_iterator.next()
        # self.data_iterator.next()
        # self.data_iterator.next()
        self.current_increment = '5min'

    def entry_conditions(self):
        print('1')
        atr = self.indicator_manager.active_indicators[('atr', '5min')]['indicator'].data
        if atr.loc[self.data_iterator.current_indices['5min']-1,'atr'] > 25:
            print('2')
            self.current_increment = '5min'
            if self.step == 0:
                if (self.close('5min', 0) > self.open('5min', 0)) and (self.close('5min', 1) > self.open('5min', 1)):
                    self.buy(self.close('5min', 0))
                    self.current_increment = '1sec'

    def exit_conditions(self):
        for _, trade in self.broker.open_trades.iterrows():
            self.current_increment = '1sec'
            if trade['profit'] > 15:

                if True:
                    self.sell(trade['entry_price'] + 10, trade_id=trade['id'])
                    self.current_increment = '5min'
                    self.step = 0
                else:
                    self.sell(self.close('1sec', 0), trade_id=trade['id'])
                    self.current_increment = '5min'
                    self.step = 0

            if trade['profit'] < -15:

                if True:
                    trade['entry_price'] - 10
                    self.sell(trade['entry_price'] - 10, trade_id=trade['id'])
                    self.current_increment = '5min'
                    self.step = 0
                else:
                    self.sell(self.close('1sec', 0), trade_id=trade['id'])
                    self.current_increment = '5min'
                    self.step = 0