import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def get_stock_data(ticker_name, period="1y"):
    """Recibe un string, retorna un DataFrame"""
    ticker = yf.Ticker(ticker_name)
    return ticker.history(period)


def get_multiple_stocks(tickers, period="1y"):
    """Recibe una lista, retorna un diccionario {ticker: df}"""
    return {ticker: get_stock_data(ticker, period) for ticker in tickers}


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
        "delta": variacion_diaria,
        "volumen_actual": volumen,
        "maximo_anual": maximo,
        "minimo_anual": minimo,
    }

    return metrics


def get_chart(df, ticker_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name=ticker_name))

    fig.update_layout(
        title=f"Precio histórico - {ticker_name}",
        xaxis_title="Fecha",
        yaxis_title="Precio (USD)",
    )

    st.plotly_chart(fig, use_container_width=True)


def get_comparison_chart(dfs):
    fig = go.Figure()
    for ticker, df in dfs.items():
        precio_inicial = df["Close"].iloc[0]
        df["retorno"] = (df["Close"] - precio_inicial) / precio_inicial * 100
        fig.add_trace(
            go.Scatter(x=df.index, y=df["retorno"], mode="lines", name=ticker)
        )

        fig.update_layout(
            title="Comparacion de rendimiento",
            xaxis_title="Fecha",
            yaxis_title="Retorno (%)",
        )

    st.plotly_chart(fig, use_container_width=True)


def main():
    pass


if __name__ == "__main__":
    main()
