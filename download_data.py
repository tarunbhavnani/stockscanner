import os
import pickle
from datetime import datetime

import yfinance as yf


def download_nifty_data(
    tickers,
    start="2020-01-01",
    end=None,
    force_download=False,
):

    #########################################################
    # Cache folder
    #########################################################

    cache_folder = r"C:\Users\tarun\Desktop\stock_scanner\data"

    os.makedirs(cache_folder, exist_ok=True)

    today = datetime.today().strftime("%Y-%m-%d")

    cache_file = os.path.join(
        cache_folder,
        f"stocks_data_{today}.pkl"
    )

    #########################################################
    # Load today's cache
    #########################################################

    if os.path.exists(cache_file) and not force_download:

        print(f"Loading cached data : {cache_file}")

        with open(cache_file, "rb") as f:
            return pickle.load(f)

    #########################################################
    # Download
    #########################################################

    print("Downloading fresh data...")

    data = {}

    for ticker in tickers:

        print(f"Downloading {ticker}")

        try:

            df = yf.download(
                ticker,
                start=start,
                end=end,
                progress=False,
                auto_adjust=True,
            )

            if df.empty:
                continue

            #################################################
            # Fix MultiIndex
            #################################################

            if hasattr(df.columns, "levels"):
                df.columns = df.columns.get_level_values(0)

            df = df[["Close", "High", "Low", "Open", "Volume"]]

            df["date"] = df.index
            df.reset_index(drop=True, inplace=True)

            df["Ticker"] = ticker

            df = df.sort_values("date")

            #################################################
            # Moving Averages
            #################################################

            df["SMA25"] = df["Close"].rolling(25).mean()
            df["SMA100"] = df["Close"].rolling(100).mean()
            df["SMA200"] = df["Close"].rolling(200).mean()

            #################################################
            # Volume MA
            #################################################

            df["VOL25"] = df["Volume"].rolling(25).mean()

            #################################################
            # Distance
            #################################################

            df["Dist25"] = (
                (df["Close"] - df["SMA25"])
                / df["SMA25"]
                * 100
            )

            df["Dist100"] = (
                (df["Close"] - df["SMA100"])
                / df["SMA100"]
                * 100
            )

            df["Dist200"] = (
                (df["Close"] - df["SMA200"])
                / df["SMA200"]
                * 100
            )

            data[ticker] = df

        except Exception as e:

            print(f"{ticker} : {e}")

    #########################################################
    # Save today's cache
    #########################################################

    with open(cache_file, "wb") as f:
        pickle.dump(data, f)

    print(f"Saved cache : {cache_file}")

    return data