import streamlit as st
from utils import (
    get_stock_data,
    get_metrics,
    get_chart,
    get_multiple_stocks,
    get_comparison_chart,
    get_forecast,
    get_forecast_chart,
)

st.set_page_config(page_title="Market Pulse", page_icon="📈")


def show_metrics(df):
    metrics = get_metrics(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        precio = f"${metrics['actual_price']:.2f}"
        delta = f"{metrics['delta']:+.2f}%"

        st.metric(label="Current Price", value=precio, delta=delta)

    with col2:
        volumen = f"{metrics['volumen_actual'] / 1_000_000:.1f}M"
        st.metric(label="Volume", value=volumen)

    with col3:
        max_val = f"${metrics['maximo_anual']:.2f}"
        st.metric(label="Annual High", value=max_val)

    with col4:
        min_val = f"${metrics['minimo_anual']:.2f}"
        st.metric(label="Annual Low", value=min_val)


def show_metrics_short(df):
    metrics = get_metrics(df)

    precio = f"${metrics['actual_price']:.2f}"
    delta = f"{metrics['delta']:+.2f}%"

    st.metric(label="Current Price", value=precio, delta=delta)


def main():
    st.title("Market Pulse")
    st.markdown("")
    ticker_name = st.multiselect(
        label="Select stocks to compare",
        options=["AAPL", "GOOGL", "TSLA", "NVDA", "MSFT", "META", "AMZN"],
        default=["AAPL"],
    )

    if not ticker_name:
        st.info("Enter a ticker to start")
        st.stop()
    else:
        if len(ticker_name) == 1:
            df = get_stock_data(ticker_name[0])
            show_metrics(df)
            chart = get_chart(df, ticker_name[0])
            st.plotly_chart(chart, width="stretch")
            forecast = get_forecast(df)
            forecast_chart = get_forecast_chart(df, forecast, ticker_name[0])
            st.plotly_chart(forecast_chart, width="stretch")
        else:
            dfs = get_multiple_stocks(ticker_name)
            cols = st.columns(len(dfs))
            for i, (ticker, df) in enumerate(dfs.items()):
                with cols[i]:
                    st.write(ticker)
                    show_metrics_short(df)
            comparison_chart = get_comparison_chart(dfs)
            st.plotly_chart(comparison_chart, width="stretch")


if __name__ == "__main__":
    main()
