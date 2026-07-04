import pandas as pd
import numpy as np


def create_scanner(data):

    rows = []

    for ticker, df in data.items():

        if len(df) < 200:
            continue

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        row = {}

        ###########################################################
        # Basic Information
        ###########################################################

        row["Ticker"] = ticker
        row["Date"] = latest["date"]

        row["Close"] = round(float(latest["Close"]), 2)

        row["25 DMA"] = round(float(latest["SMA25"]), 2)
        row["100 DMA"] = round(float(latest["SMA100"]), 2)
        row["200 DMA"] = round(float(latest["SMA200"]), 2)

        row["Volume"] = int(latest["Volume"])
        row["25 Vol MA"] = int(latest["VOL25"])

        ###########################################################
        # Distance From MA
        ###########################################################

        row["Dist25 %"] = round(float(latest["Dist25"]), 2)
        row["Dist100 %"] = round(float(latest["Dist100"]), 2)
        row["Dist200 %"] = round(float(latest["Dist200"]), 2)

        ###########################################################
        # Above / Below Moving Average
        ###########################################################

        row["Above25"] = latest["Close"] > latest["SMA25"]
        row["Above100"] = latest["Close"] > latest["SMA100"]
        row["Above200"] = latest["Close"] > latest["SMA200"]

        ###########################################################
        # Volume
        ###########################################################

        row["AboveVol25"] = latest["Volume"] > latest["VOL25"]

        ###########################################################
        # Trend
        ###########################################################

        row["AboveAll"] = (
            row["Above25"]
            and row["Above100"]
            and row["Above200"]
        )

        row["BelowAll"] = (
            not row["Above25"]
            and not row["Above100"]
            and not row["Above200"]
        )

        ###########################################################
        # Combination Filters
        ###########################################################

        row["Above25_100"] = (
            row["Above25"]
            and row["Above100"]
        )

        row["Above100_200"] = (
            row["Above100"]
            and row["Above200"]
        )

        row["Above25_200"] = (
            row["Above25"]
            and row["Above200"]
        )

        ###########################################################
        # Fresh Crossovers
        ###########################################################

        row["Crossed Above 25"] = (
            prev["Close"] < prev["SMA25"]
            and latest["Close"] > latest["SMA25"]
        )

        row["Crossed Above 100"] = (
            prev["Close"] < prev["SMA100"]
            and latest["Close"] > latest["SMA100"]
        )

        row["Crossed Above 200"] = (
            prev["Close"] < prev["SMA200"]
            and latest["Close"] > latest["SMA200"]
        )

        ###########################################################
        # Fresh Breakdown
        ###########################################################

        row["Crossed Below 25"] = (
            prev["Close"] > prev["SMA25"]
            and latest["Close"] < latest["SMA25"]
        )

        row["Crossed Below 100"] = (
            prev["Close"] > prev["SMA100"]
            and latest["Close"] < latest["SMA100"]
        )

        row["Crossed Below 200"] = (
            prev["Close"] > prev["SMA200"]
            and latest["Close"] < latest["SMA200"]
        )

        ###########################################################
        # Golden Cross
        ###########################################################

        row["Golden Cross"] = (
            prev["SMA25"] < prev["SMA200"]
            and latest["SMA25"] > latest["SMA200"]
        )

        ###########################################################
        # Death Cross
        ###########################################################

        row["Death Cross"] = (
            prev["SMA25"] > prev["SMA200"]
            and latest["SMA25"] < latest["SMA200"]
        )

        ###########################################################
        # Volume Spike
        ###########################################################

        row["1.5x Volume"] = (
            latest["Volume"] > latest["VOL25"] * 1.5
        )

        row["2x Volume"] = (
            latest["Volume"] > latest["VOL25"] * 2
        )

        ###########################################################
        # 52 Week High / Low
        ###########################################################

        high52 = df["High"].tail(252).max()
        low52 = df["Low"].tail(252).min()

        row["52 Week High"] = latest["Close"] >= high52
        row["52 Week Low"] = latest["Close"] <= low52

        rows.append(row)

    scanner = pd.DataFrame(rows)

    scanner = scanner.sort_values(
        "Ticker"
    ).reset_index(drop=True)

    return scanner