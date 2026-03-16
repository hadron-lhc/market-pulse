import streamlit as st
import yfinance as yf
from utils import get_stock_data, get_metrics


def show_metrics(df):
    metrics = get_metrics(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        precio = f"${metrics['actual_price']:.2f}"
        delta = f"{metrics['delta']:+.2f}%"

        st.metric(label="Precio actual", value=precio, delta=delta)

    with col2:
        volumen = f"{metrics['volumen_actual'] / 1_000_000:.1f}M"
        st.metric(label="Volumen", value=volumen)

    with col3:
        max_val = f"${metrics['maximo_anual']:.2f}"
        st.metric(label="Maximo anual", value=max_val)

    with col4:
        min_val = f"${metrics['minimo_anual']:.2f}"
        st.metric(label="Minimo anual", value=min_val)


def main():
    st.title("Market Pulse")
    st.markdown("")
    ticker_name = st.text_input("Ingrese un ticker")
    if not ticker_name:
        st.info("Ingresá un ticker para comenzar")
        st.stop()
    else:
        df = get_stock_data(ticker_name)
        show_metrics(df)


if __name__ == "__main__":
    main()
