import plotly.graph_objects as go
import pandas as pd


def draw_chart(df):

    # Make sure date column is datetime
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Show only last 6 months
    last_date = df["date"].max()
    start_date = last_date - pd.DateOffset(months=6)

    df = df[df["date"] >= start_date]

    fig = go.Figure()

    # Close Price
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["Close"],
            name="Close",
            line=dict(width=2)
        )
    )

    # 25 DMA
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["SMA25"],
            name="25 DMA"
        )
    )

    # 100 DMA
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["SMA100"],
            name="100 DMA"
        )
    )

    # 200 DMA
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["SMA200"],
            name="200 DMA"
        )
    )

    fig.update_layout(
        title="Last 6 Months",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        template="plotly_white",
        legend_orientation="h",
        legend=dict(y=1.02, x=0),
        margin=dict(l=20, r=20, t=50, b=20),
        height=600
    )

    return fig