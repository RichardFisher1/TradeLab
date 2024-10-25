import pandas as pd
import pandas_ta as ta

# Sample data: Replace with your own DataFrame
data = {
    'Date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'Open': pd.Series(range(100)).apply(lambda x: 100 + x),
    'High': pd.Series(range(100)).apply(lambda x: 105 + x),
    'Low': pd.Series(range(100)).apply(lambda x: 95 + x),
    'Close': pd.Series(range(100)).apply(lambda x: 100 + x)
}
df = pd.DataFrame(data)

# Set 'Date' as the index if you want to use it as the time index
df.set_index('Date', inplace=True)

# Calculate the ATR
atr_period = 14  # Set the ATR period
df['ATR'] = ta.atr(high=df['High'], low=df['Low'], close=df['Close'], length=atr_period)

print(df[['High', 'Low', 'Close', 'ATR']].tail())
