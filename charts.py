import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def draw_chart(df, period="6M"):

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    ###########################################################
    # Filter Period
    ###########################################################

    last_date = df["date"].max()

    if period == "3M":
        start = last_date - pd.DateOffset(months=3)

    elif period == "6M":
        start = last_date - pd.DateOffset(months=6)

    elif period == "1Y":
        start = last_date - pd.DateOffset(years=1)

    else:
        start = df["date"].min()

    df = df[df["date"] >= start]

    ###########################################################
    # Create Figure
    ###########################################################

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25]
    )

    ###########################################################
    # Candlestick
    ###########################################################

    fig.add_trace(

        go.Candlestick(

            x=df["date"],

            open=df["Open"],

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            name="Price"

        ),

        row=1,
        col=1

    )

    ###########################################################
    # Moving Averages
    ###########################################################

    fig.add_trace(

        go.Scatter(

            x=df["date"],

            y=df["SMA25"],

            name="25 DMA",

            line=dict(width=1.5)

        ),

        row=1,
        col=1

    )

    fig.add_trace(

        go.Scatter(

            x=df["date"],

            y=df["SMA100"],

            name="100 DMA",

            line=dict(width=1.5)

        ),

        row=1,
        col=1

    )

    fig.add_trace(

        go.Scatter(

            x=df["date"],

            y=df["SMA200"],

            name="200 DMA",

            line=dict(width=1.5)

        ),

        row=1,
        col=1

    )

    ###########################################################
    # Volume
    ###########################################################

    colors = []

    for _, row in df.iterrows():

        if row["Close"] >= row["Open"]:
            colors.append("green")
        else:
            colors.append("red")

    fig.add_trace(

        go.Bar(

            x=df["date"],

            y=df["Volume"],

            marker_color=colors,

            name="Volume"

        ),

        row=2,
        col=1

    )

    ###########################################################
    # Average Volume
    ###########################################################

    fig.add_trace(

        go.Scatter(

            x=df["date"],

            y=df["VOL25"],

            name="25 Vol MA",

            line=dict(color="orange", width=2)

        ),

        row=2,
        col=1

    )

    ###########################################################
    # Layout
    ###########################################################

    fig.update_layout(

        template="plotly_white",

        height=750,

        hovermode="x unified",

        xaxis_rangeslider_visible=False,

        legend=dict(

            orientation="h",

            y=1.02,

            x=0

        ),

        margin=dict(

            l=20,

            r=20,

            t=40,

            b=20

        )

    )

    fig.update_yaxes(title="Price", row=1, col=1)

    fig.update_yaxes(title="Volume", row=2, col=1)

    return fig