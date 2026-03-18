import yfinance as yf
import plotly.graph_objects as go
from prophet import Prophet


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

    return fig


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

    return fig


def get_forecast(df, days=30):
    df_prophet = df[["Close"]].copy()
    df_prophet = df_prophet.reset_index()  # Date pasa a ser columna
    df_prophet.columns = ["ds", "y"]  # renombrás las columnas
    df_prophet["ds"] = df_prophet["ds"].dt.tz_localize(None)  # sacás timezone

    model = Prophet(
        daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=True
    )

    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=days)

    # Predecir
    forecast = model.predict(future)

    return forecast


def get_forecast_chart(df, forecast, ticker):
    ultima_fecha = df.index[-1].tz_localize(None)
    forecast_futuro = forecast[forecast["ds"] > ultima_fecha]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name=ticker))
    fig.add_trace(
        go.Scatter(
            x=forecast_futuro["ds"],
            y=forecast_futuro["yhat_upper"],
            mode="lines",
            line=dict(width=0),  # línea invisible
            name="Intervalo superior",
        )
    )

    # Después el límite inferior — se rellena HACIA el trace anterior (yhat_upper)
    fig.add_trace(
        go.Scatter(
            x=forecast_futuro["ds"],
            y=forecast_futuro["yhat_lower"],
            mode="lines",
            line=dict(width=0),  # línea invisible
            fill="tonexty",  # rellena hasta el trace de arriba
            fillcolor="rgba(99, 110, 250, 0.3)",  # azul transparente
            name="Intervalo de confianza",
        )
    )

    # Finalmente la línea de predicción encima
    fig.add_trace(
        go.Scatter(
            x=forecast_futuro["ds"],
            y=forecast_futuro["yhat"],
            mode="lines",
            name="Predicción",
        )
    )

    fig.update_layout(
        title=f"Prediccion - {ticker}",
        xaxis_title="Fecha",
        yaxis_title="Precio (USD)",
    )

    return fig


def main():
    df = get_stock_data("AAPL")
    forecast = get_forecast(df)
    print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10))


if __name__ == "__main__":
    main()
