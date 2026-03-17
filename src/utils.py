import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def get_stock_data(ticker_name, period="1y"):
    ticker = yf.Ticker(ticker_name)
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
        "delta": variacion_diaria,
        "volumen_actual": volumen,
        "maximo_anual": maximo,
        "minimo_anual": minimo,
    }

    return metrics


def get_chart(ticker_name):
    df = get_stock_data(ticker_name)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name=ticker_name))

    fig.update_layout(
        title=f"Precio histórico - {ticker_name}",
        xaxis_title="Fecha",
        yaxis_title="Precio (USD)",
    )

    st.plotly_chart(fig, use_container_width=True)


def main():
    pass


if __name__ == "__main__":
    main()
