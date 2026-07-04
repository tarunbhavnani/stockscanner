import streamlit as st
import pandas as pd

from download_data import download_nifty_data
from scanner import create_scanner
from charts import draw_chart


###########################################################################
# PAGE CONFIG
###########################################################################

st.set_page_config(
    page_title="Nifty Stock Scanner",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Nifty Stock Scanner")

###########################################################################
# NIFTY STOCKS
###########################################################################

"""
nifty = [
'TATACONSUM.NS','BAJFINANCE.NS','WIPRO.NS','ASIANPAINT.NS',
'HINDALCO.NS','CIPLA.NS','ETERNAL.NS','APOLLOHOSP.NS',
'DRREDDY.NS','SHRIRAMFIN.NS','BHARTIARTL.NS','HDFCLIFE.NS',
'TRENT.NS','EICHERMOT.NS','NESTLEIND.NS','INDIGO.NS',
'HDFCBANK.NS','RELIANCE.NS','SUNPHARMA.NS','BAJAJFINSV.NS',
'MAXHEALTH.NS','M&M.NS','MARUTI.NS','TITAN.NS',
'BAJAJ-AUTO.NS','ADANIPORTS.NS','SBILIFE.NS','SBIN.NS',
'ADANIENT.NS','POWERGRID.NS','JIOFIN.NS','HCLTECH.NS',
'HINDUNILVR.NS','JSWSTEEL.NS','TCS.NS','COALINDIA.NS',
'INFY.NS','ICICIBANK.NS','ITC.NS','AXISBANK.NS',
'ULTRACEMCO.NS','ONGC.NS','BEL.NS','NTPC.NS',
'KOTAKBANK.NS'
]
"""
nifty=['TRIDENT.NS', 'COHANCE.NS', 'SUVEN.NS', 'SWANCORP.NS',
         'MOTHERSON.NS', 'TIMETECHNO.NS', 'JIOFIN.NS', 'RELIANCE.NS', 'DABUR.NS',
         'SAGILITY.NS', 'VEDL.NS', 'DELTACORP.NS', 'IOC.NS', 'GOCOLORS.NS',
         "ABFRL.NS","ABLBL.NS","NETWORK18.NS"]


###########################################################################
# CACHE DATA
###########################################################################

@st.cache_data(show_spinner=True)
def load_data():

    return download_nifty_data(
        nifty,
        start="2020-01-01"
    )


data = load_data()

scanner = create_scanner(data)

###########################################################################
# MARKET BREADTH
###########################################################################

st.subheader("Market Breadth")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Above 25 DMA",
    int(scanner["Above25"].sum())
)

c2.metric(
    "Above 100 DMA",
    int(scanner["Above100"].sum())
)

c3.metric(
    "Above 200 DMA",
    int(scanner["Above200"].sum())
)

c4.metric(
    "Above All",
    int(scanner["AboveAll"].sum())
)

c5.metric(
    "Below All",
    int(scanner["BelowAll"].sum())
)

c6.metric(
    "Vol > 25MA",
    int(scanner["AboveVol25"].sum())
)

st.divider()

###########################################################################
# SIDEBAR
###########################################################################

st.sidebar.title("Scanner")

###########################################################################
# PRICE FILTERS
###########################################################################

st.sidebar.subheader("Moving Average")

price_filters = st.sidebar.multiselect(

    "Price",

    [

        "Above 25 DMA",

        "Above 100 DMA",

        "Above 200 DMA",

        "Above All",

        "Below All"

    ]

)

###########################################################################
# VOLUME
###########################################################################

st.sidebar.subheader("Volume")

volume_filters = st.sidebar.multiselect(

    "Volume",

    [

        "Above 25 Vol MA",

        "1.5x Volume",

        "2x Volume"

    ]

)

###########################################################################
# CROSSOVERS
###########################################################################

st.sidebar.subheader("Crossovers")

cross_filters = st.sidebar.multiselect(

    "Crossovers",

    [

        "Cross Above 25",

        "Cross Above 100",

        "Cross Above 200",

        "Cross Below 25",

        "Cross Below 100",

        "Cross Below 200",

        "Golden Cross",

        "Death Cross"

    ]

)

###########################################################################
# 52 WEEK
###########################################################################

st.sidebar.subheader("52 Week")

week_filters = st.sidebar.multiselect(

    "52 Week",

    [

        "52 Week High",

        "52 Week Low"

    ]

)

###########################################################################
# SEARCH
###########################################################################

search = st.sidebar.text_input(
    "Search Stock"
)

###########################################################################
# FILTER DATAFRAME
###########################################################################

filtered = scanner.copy()

#####################################################
# SEARCH
#####################################################

if search != "":

    filtered = filtered[
        filtered["Ticker"].str.contains(
            search.upper()
        )
    ]

#####################################################
# PRICE
#####################################################

for item in price_filters:

    if item == "Above 25 DMA":
        filtered = filtered[filtered["Above25"]]

    elif item == "Above 100 DMA":
        filtered = filtered[filtered["Above100"]]

    elif item == "Above 200 DMA":
        filtered = filtered[filtered["Above200"]]

    elif item == "Above All":
        filtered = filtered[filtered["AboveAll"]]

    elif item == "Below All":
        filtered = filtered[filtered["BelowAll"]]

#####################################################
# VOLUME
#####################################################

for item in volume_filters:

    if item == "Above 25 Vol MA":
        filtered = filtered[
            filtered["AboveVol25"]
        ]

    elif item == "1.5x Volume":
        filtered = filtered[
            filtered["1.5x Volume"]
        ]

    elif item == "2x Volume":
        filtered = filtered[
            filtered["2x Volume"]
        ]

#####################################################
# CROSSOVERS
#####################################################

for item in cross_filters:

    if item == "Cross Above 25":
        filtered = filtered[
            filtered["Crossed Above 25"]
        ]

    elif item == "Cross Above 100":
        filtered = filtered[
            filtered["Crossed Above 100"]
        ]

    elif item == "Cross Above 200":
        filtered = filtered[
            filtered["Crossed Above 200"]
        ]

    elif item == "Cross Below 25":
        filtered = filtered[
            filtered["Crossed Below 25"]
        ]

    elif item == "Cross Below 100":
        filtered = filtered[
            filtered["Crossed Below 100"]
        ]

    elif item == "Cross Below 200":
        filtered = filtered[
            filtered["Crossed Below 200"]
        ]

    elif item == "Golden Cross":
        filtered = filtered[
            filtered["Golden Cross"]
        ]

    elif item == "Death Cross":
        filtered = filtered[
            filtered["Death Cross"]
        ]

#####################################################
# 52 WEEK
#####################################################

for item in week_filters:

    if item == "52 Week High":
        filtered = filtered[
            filtered["52 Week High"]
        ]

    elif item == "52 Week Low":
        filtered = filtered[
            filtered["52 Week Low"]
        ]
###########################################################################
# SORTING
###########################################################################

st.subheader("Scanner Results")

sort_column = st.selectbox(

    "Sort By",

    [

        "Ticker",
        "Close",
        "Dist25 %",
        "Dist100 %",
        "Dist200 %",
        "Volume"

    ]

)

ascending = st.checkbox(
    "Ascending",
    value=True
)

filtered = filtered.sort_values(
    sort_column,
    ascending=ascending
)

###########################################################################
# DISPLAY COLUMNS
###########################################################################

display_columns = [

    "Ticker",

    "Close",

    "25 DMA",
    "100 DMA",
    "200 DMA",

    "Dist25 %",
    "Dist100 %",
    "Dist200 %",

    "Volume",
    "25 Vol MA",

    "Above25",
    "Above100",
    "Above200",

    "AboveVol25"

]

###########################################################################
# CONDITIONAL FORMATTING
###########################################################################

def colour_boolean(v):

    if isinstance(v, bool):

        if v:
            return "background-color:#b7f7b7"

        return "background-color:#ffb3b3"

    return ""


styled = (
    filtered[display_columns]
    .style
    .applymap(
        colour_boolean,
        subset=[
            "Above25",
            "Above100",
            "Above200",
            "AboveVol25"
        ]
    )
)

st.dataframe(

    styled,

    use_container_width=True,

    height=500

)

###########################################################################
# DOWNLOAD CSV
###########################################################################

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(

    "Download Scanner",

    csv,

    file_name="scanner.csv",

    mime="text/csv"

)

###########################################################################
# CHART
###########################################################################

st.divider()

st.subheader("Chart")

if len(filtered) == 0:

    st.warning("No stocks satisfy the selected filters.")

else:

    col1, col2 = st.columns([2, 1])

    with col1:

        stock = st.selectbox(

            "Stock",

            filtered["Ticker"]

        )

    with col2:

        period = st.selectbox(

            "Chart Period",

            [

                "3M",

                "6M",

                "1Y",

                "All"

            ],

            index=1

        )

    fig = draw_chart(

        data[stock],

        period

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

###########################################################################
# SUMMARY
###########################################################################

st.divider()

st.subheader("Summary")

c1, c2, c3 = st.columns(3)

c1.metric(

    "Stocks Displayed",

    len(filtered)

)

if len(filtered):

    c2.metric(

        "Average Distance from 25 DMA",

        f"{filtered['Dist25 %'].mean():.2f}%"

    )

    c3.metric(

        "Average Distance from 200 DMA",

        f"{filtered['Dist200 %'].mean():.2f}%"

    )

###########################################################################
# REFRESH
###########################################################################

st.sidebar.divider()

if st.sidebar.button("🔄 Refresh Data"):

    st.cache_data.clear()

    st.rerun()