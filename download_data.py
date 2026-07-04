import yfinance as yf


def download_nifty_data(tickers, start="2020-01-01", end=None):

    data = {}

    for ticker in tickers:

        print("Downloading", ticker)

        df = yf.download(
            ticker,
            start=start,
            end=end,
            progress=False
        )

        if len(df) == 0:
            continue

        df.columns = [
            "Close",
            "High",
            "Low",
            "Open",
            "Volume"
        ]

        df["date"] = df.index
        df.reset_index(drop=True, inplace=True)

        df["Ticker"] = ticker

        df = df.sort_values("date")

        # Moving averages
        df["SMA25"] = df.Close.rolling(25).mean()
        df["SMA100"] = df.Close.rolling(100).mean()
        df["SMA200"] = df.Close.rolling(200).mean()

        # Volume average
        df["VOL25"] = df.Volume.rolling(25).mean()

        data[ticker] = df

    return data