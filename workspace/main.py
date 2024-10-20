from utils.data_import import import_data
from tradelab.gui import ChartsApp
import pandas as pd


# Market configuration
market_config = {
    'date_range': ('2024-04-19', '2024-05-09'),
    'time_range': ('14:00:00', '17:00:00'),
    'market': 'wallstreet',
    'timeframes': ['1sec','1min', '5min']
}

# Load market data
data = import_data(market_config)

# Run
app = ChartsApp(data)
app.run()



# FIX SAVING WORKSPACE
# FIX COLOUR SETTING FOR INDICATORS
# FIX SPEED CONTROL OF SIMULATION 




#ML
# use cnn to learn pattern for single case - use to signal similar instances. use indicators to focus on particular contexts 