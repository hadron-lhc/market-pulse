import yfinance as yf
import pandas as pd


def get_stock_data(ticker, period="1y"):
    df = ticker.history(period)
    return df


def get_metrics(df):
    precio_actual = df["Close"].iloc[-1]
    precio_ayer = df["Close"].iloc[-2]
    variacion_diaria = (precio_actual - precio_ayer) / precio_ayer * 100
    volumen = df["Volume"].iloc[-1]
    maximo = df["High"].max()
    minimo = df["Low"].min()

    metrics = {
        "actual_price": precio_actual,
        "past_price": precio_ayer,
        "Varacion_diaria": variacion_diaria,
        "volumen_actual": volumen,
        "maximo_anual": maximo,
        "minimo_anual": minimo,
    }

    return metrics


def main():
    ticker = yf.Ticker("AAPL")
    df = get_stock_data(ticker)
    print(df.head())


if __name__ == "__main__":
    main()
