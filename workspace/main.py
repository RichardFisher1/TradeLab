from utils.data_import import import_data
from tradelab.gui import ChartsApp

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


