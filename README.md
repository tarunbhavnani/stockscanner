# 📈 Nifty Stock Scanner

A professional **Streamlit-based stock scanner** for Indian equities that analyzes Nifty stocks using moving averages, volume, and technical trend filters. The dashboard provides an interactive interface to identify stocks meeting custom technical criteria and visualize them using Plotly candlestick charts.

---

## Features

### Market Breadth

* Number of stocks above 25 DMA
* Number of stocks above 100 DMA
* Number of stocks above 200 DMA
* Stocks above all moving averages
* Stocks below all moving averages
* Stocks trading above 25-day average volume

---

### Technical Scanners

#### Moving Average Filters

* Above 25 DMA
* Above 100 DMA
* Above 200 DMA
* Above All DMAs
* Below All DMAs

#### Volume Filters

* Volume above 25-day average
* 1.5× Average Volume
* 2× Average Volume

#### Crossovers

* Crossed Above 25 DMA
* Crossed Above 100 DMA
* Crossed Above 200 DMA
* Crossed Below 25 DMA
* Crossed Below 100 DMA
* Crossed Below 200 DMA
* Golden Cross
* Death Cross

#### 52-Week Filters

* 52 Week High
* 52 Week Low

---

## Interactive Dashboard

* Multi-select scanner filters
* Stock search
* Sortable scanner table
* Download results as CSV
* Interactive Plotly charts
* Candlestick chart
* 25 DMA
* 100 DMA
* 200 DMA
* Volume
* 25-day Volume Moving Average
* Chart period selection

  * 3 Months
  * 6 Months
  * 1 Year
  * All Data

---

## Project Structure

```text
StockScanner/
│
├── app.py
├── charts.py
├── scanner.py
├── download_data.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your_username>/StockScanner.git
```

Move into the project folder

```bash
cd StockScanner
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Streamlit dashboard

```bash
streamlit run app.py
```

The application will open automatically in your browser.

If it does not open automatically, visit

```
http://localhost:8501
```

---

## Technologies Used

* Python
* Streamlit
* Plotly
* Pandas
* NumPy
* yfinance

---

## Data Source

Market data is downloaded using the `yfinance` library.

---

## Future Enhancements

Planned additions include:

* RSI Scanner
* MACD Scanner
* ADX Scanner
* Supertrend
* VWAP
* Bollinger Bands
* Relative Strength Ranking
* ATR Scanner
* Sector Heatmap
* Market Breadth Charts
* TradingView-style Heatmap
* Order Block Detection
* Fair Value Gap Detection
* Candlestick Pattern Recognition
* Support & Resistance Detection
* Volume Profile
* Options Chain Analysis
* Portfolio Dashboard
* Backtesting Engine
* Telegram Alerts
* AI-powered Stock Ranking

---

## Screenshots

You can add screenshots here after running the application.

Example:

```
images/dashboard.png
images/chart.png
```

---

## License

This project is licensed under the MIT License.

---

## Disclaimer

This project is intended for educational and research purposes only.

It should not be considered financial or investment advice. Always perform your own analysis before making investment decisions.
