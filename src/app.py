import streamlit as st
import yfinance as yf
from utils import get_stock_data


def main():
    st.title("YFinance")
    st.markdown("")
    ticker_name = st.text_input("Ingrese un ticker")
    if ticker_name != "":
        ticker = yf.Ticker(ticker_name)
        df = get_stock_data(ticker)
        st.write(df)


if __name__ == "__main__":
    main()
