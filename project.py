import os
import pandas as pd
import matplotlib.pyplot as plt

path = "/Users/jacobpark/Documents/CSpractice/data"
stock = 'tsla'

def test_run():
    # Read data
    dates = pd.date_range('2013-3-21', '2017-03-17')
    symbols = [stock]

    df = get_data(symbols, dates)

    # Normalize the stock to the initial price point
    df = df / df.ix[0,:]

    # Compute rolling mean for stock
    rm = get_rolling_mean(df[stock], 20)

    # plot the data
    plot_data(df, rm)

def plot_data(df, rm, title="Stock & SPY"):
        # Plot raw SPY values, rolling mean and Bollinger Bands
        ax = df.plot(title=title, label=stock)
        rm.plot()
        # Add axis labels and legend
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend(loc='upper left')
        plt.show()

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)

    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == stock:  # drop dates SPY did not trade
            df = df.dropna(subset=[stock])
    return df

def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.rolling_mean(values, window=window)


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return pd.rolling_std(values, window=window)

def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + 2*rstd
    lower_band = rm - 2*rstd
    return upper_band, lower_band


def symbol_to_path(symbol, base_dir=path):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

if __name__ == "__main__":

    test_run()
