import yfinance as yf


def download_nifty_data(tickers, start="2020-01-01", end=None):

    data = {}

    for ticker in tickers:

        print(f"Downloading {ticker}")

        try:

            df = yf.download(
                ticker,
                start=start,
                end=end,
                progress=False,
                auto_adjust=True
            )

            if df.empty:
                continue

            # Handle MultiIndex columns if returned
            if hasattr(df.columns, "levels"):
                df.columns = df.columns.get_level_values(0)

            df = df.rename(columns={
                "Close": "Close",
                "High": "High",
                "Low": "Low",
                "Open": "Open",
                "Volume": "Volume"
            })

            df = df[["Close", "High", "Low", "Open", "Volume"]]

            df["date"] = df.index
            df.reset_index(drop=True, inplace=True)

            df["Ticker"] = ticker

            df = df.sort_values("date")

            ###########################
            # Moving Averages
            ###########################

            df["SMA25"] = df["Close"].rolling(25).mean()
            df["SMA100"] = df["Close"].rolling(100).mean()
            df["SMA200"] = df["Close"].rolling(200).mean()

            ###########################
            # Volume MA
            ###########################

            df["VOL25"] = df["Volume"].rolling(25).mean()

            ###########################
            # Distance from MA
            ###########################

            df["Dist25"] = (
                (df["Close"] - df["SMA25"])
                / df["SMA25"] * 100
            )

            df["Dist100"] = (
                (df["Close"] - df["SMA100"])
                / df["SMA100"] * 100
            )

            df["Dist200"] = (
                (df["Close"] - df["SMA200"])
                / df["SMA200"] * 100
            )

            data[ticker] = df

        except Exception as e:
            print(e)

    return data