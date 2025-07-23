import yfinance as yf
import pandas as pd
from datetime import datetime

def download_and_clean_data(tickers, years=15):
    end_date = datetime.now()
    start_date = datetime(end_date.year - years, end_date.month, end_date.day)
    print(f"Downloading historical data for {len(tickers)} tickers...")
    prices_df = yf.download(tickers, start=start_date, end=end_date)['Close']
    prices_df.dropna(axis=1, thresh=len(prices_df) * 0.9, inplace=True)
    prices_df.dropna(axis=0, how='any', inplace=True)
    tickers_final = prices_df.columns.tolist()
    print("\nDownload and cleaning completed!")
    print(f"Final dataset contains {len(tickers_final)} tickers and {len(prices_df)} days of data.")
    print("Preview:")
    print(prices_df.head())
    return prices_df, tickers_final, start_date, end_date

# Static NASDAQ-100 ticker list
TICKERS = [
    'MSFT', 'AAPL', 'NVDA', 'AMZN', 'META', 'AVGO', 'GOOGL', 'TSLA', 'GOOG',
    'COST', 'AMD', 'NFLX', 'PEP', 'ADBE', 'LIN', 'CSCO', 'TMUS', 'INTC',
    'CMCSA', 'QCOM', 'INTU', 'AMGN', 'TXN', 'HON', 'AMAT', 'BKNG', 'LRCX',
    'ISRG', 'ADI', 'VRTX', 'REGN', 'SBUX', 'ADP', 'MDLZ', 'PANW', 'MU',
    'PYPL', 'SNPS', 'KLAC', 'CDNS', 'ASML', 'GILD', 'MELI', 'CRWD', 'CSX',
    'MAR', 'CTAS', 'ORLY', 'PCAR', 'MRNA', 'ABNB', 'WDAY', 'ROP', 'FTNT',
    'CEG', 'PAYX', 'FAST', 'DXCM', 'BIIB', 'KDP', 'AEP', 'DDOG', 'EXC',
    'MNST', 'CPRT', 'IDXX', 'LULU', 'TEAM', 'BKR', 'MCHP', 'AZN', 'EA',
    'MRVL', 'CTSH', 'KHC', 'GEHC', 'ROST', 'WBA', 'ODFL', 'ON',
    'CSGP', 'XEL', 'FANG', 'DLTR', 'ANSS', 'TTD', 'PCG', 'MDB', 'ILMN',
    'ZS', 'WBD', 'SIRI', 'ALGN', 'ENPH', 'JD', 'LCID'
] 