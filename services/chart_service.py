import matplotlib
matplotlib.use("Agg")

import os
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

def create_stock_chart(df, stock_code):
    df_chart = df.copy()
    df_chart = df_chart.tail(60)

    df_chart.index = pd.to_datetime(df_chart["日期"])

    df_chart = df_chart.rename(columns={
        "開盤價": "Open",
        "最高價": "High",
        "最低價": "Low",
        "收盤價": "Close",
        "成交股數": "Volume"
    })

    os.makedirs("static/charts", exist_ok=True)

    chart_path = f"static/charts/{stock_code}.png"
    mpf.plot(
        df_chart,
        type="candle",
        mav=(5, 20),
        volume=True,
        figsize=(12, 8),
        tight_layout=True,
        savefig=chart_path
    )

    plt.close("all")

    return f"{stock_code}.png"