import pandas as pd


def create_scanner(data):

    rows = []

    for ticker, df in data.items():

        latest = df.iloc[-1]

        row = {

            "Ticker": ticker,

            "Close": latest.Close,

            "25 DMA": latest.SMA25,

            "100 DMA": latest.SMA100,

            "200 DMA": latest.SMA200,

            "Volume": latest.Volume,

            "25 Vol MA": latest.VOL25,

            "Above25": latest.Close > latest.SMA25,

            "Above100": latest.Close > latest.SMA100,

            "Above200": latest.Close > latest.SMA200,

            "AboveVol25": latest.Volume > latest.VOL25,

        }

        row["AboveAll"] = (
            row["Above25"] and
            row["Above100"] and
            row["Above200"]
        )

        row["BelowAll"] = (
            not row["Above25"] and
            not row["Above100"] and
            not row["Above200"]
        )

        row["Above25_100"] = (
            row["Above25"] and row["Above100"]
        )

        row["Above100_200"] = (
            row["Above100"] and row["Above200"]
        )

        rows.append(row)

    return pd.DataFrame(rows)