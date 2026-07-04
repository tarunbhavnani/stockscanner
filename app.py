import streamlit as st

from download_data import download_nifty_data
from scanner import create_scanner
from charts import draw_chart


###########################################################################
# PAGE
###########################################################################

st.set_page_config(
    page_title="Nifty Scanner",
    layout="wide"
)

st.title("📈 Nifty Scanner")


###########################################################################
# TICKERS
###########################################################################

nifty = ['TRIDENT.NS', 'COHANCE.NS', 'SUVEN.NS', 'SWANCORP.NS',
         'MOTHERSON.NS', 'TIMETECHNO.NS', 'JIOFIN.NS', 'RELIANCE.NS', 'DABUR.NS',
         'SAGILITY.NS', 'VEDL.NS', 'DELTACORP.NS', 'IOC.NS', 'GOCOLORS.NS',
         "ABFRL.NS","ABLBL.NS"]



###########################################################################
# CACHE
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
# METRICS
###########################################################################

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric("Above 25 DMA", scanner.Above25.sum())

c2.metric("Above 100 DMA", scanner.Above100.sum())

c3.metric("Above 200 DMA", scanner.Above200.sum())

c4.metric("Above All", scanner.AboveAll.sum())

c5.metric("Below All", scanner.BelowAll.sum())

c6.metric("Volume > 25MA", scanner.AboveVol25.sum())


###########################################################################
# FILTER
###########################################################################

choice = st.sidebar.selectbox(

    "Scanner",

    [

        "All",

        "Above 25",

        "Above 100",

        "Above 200",

        "Above All",

        "Below All",

        "Above 25 & 100",

        "Above 100 & 200",

        "Above Volume"

    ]

)

filtered = scanner.copy()

if choice == "Above 25":
    filtered = filtered[filtered.Above25]

elif choice == "Above 100":
    filtered = filtered[filtered.Above100]

elif choice == "Above 200":
    filtered = filtered[filtered.Above200]

elif choice == "Above All":
    filtered = filtered[filtered.AboveAll]

elif choice == "Below All":
    filtered = filtered[filtered.BelowAll]

elif choice == "Above 25 & 100":
    filtered = filtered[filtered.Above25_100]

elif choice == "Above 100 & 200":
    filtered = filtered[filtered.Above100_200]

elif choice == "Above Volume":
    filtered = filtered[filtered.AboveVol25]


st.dataframe(
    filtered,
    use_container_width=True
)


###########################################################################
# CHART
###########################################################################

stock = st.selectbox(
    "Stock",
    filtered.Ticker
)

st.plotly_chart(
    draw_chart(data[stock]),
    use_container_width=True
)


###########################################################################
# REFRESH BUTTON
###########################################################################

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()