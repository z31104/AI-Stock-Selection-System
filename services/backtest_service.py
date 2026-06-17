import requests
import pandas as pd
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings()


def get_month_stock_data(stock_code, month_date):
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY"

    params = {
        "response": "json",
        "date": month_date,
        "stockNo": stock_code
    }

    try:

        response = requests.get(
        url,
        params=params,
        verify=False,
        timeout=10
    )

        data = response.json()

    except Exception as e:

        print("TWSE錯誤:", e)

        return None

    data = response.json()

    if "data" not in data or len(data["data"]) == 0:
        return None

    df = pd.DataFrame(data["data"], columns=data["fields"])

    df["日期"] = df["日期"].apply(
        lambda x: str(int(x.split("/")[0]) + 1911)
        + "-"
        + x.split("/")[1]
        + "-"
        + x.split("/")[2]
    )

    df["日期"] = pd.to_datetime(df["日期"])
    df["收盤價"] = df["收盤價"].str.replace(",", "").astype(float)

    return df[["日期", "收盤價"]]


def get_backtest_data(stock_code, start_date, holding_days=30):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = start + timedelta(days=holding_days)

    month_list = [
        start.strftime("%Y%m01"),
        end.strftime("%Y%m01")
    ]

    dfs = []

    for month_date in month_list:
        print(
    f"下載中: {stock_code} {month_date}"
)
        df = get_month_stock_data(stock_code, month_date)

        if df is not None:
            dfs.append(df)

    if len(dfs) == 0:
        return None

    all_df = pd.concat(dfs)
    all_df = all_df.drop_duplicates(subset=["日期"])
    all_df = all_df.sort_values("日期")

    all_df = all_df[
        (all_df["日期"] >= start) &
        (all_df["日期"] <= end)
    ]

    if len(all_df) < 2:
        return None

    return all_df

def run_real_backtest(records, capital, start_date, holding_days=30):
    if records is None or len(records) == 0:
        return {
            "results": [],
            "portfolio_dates": [],
            "portfolio_values": []
        }

    selected = sorted(
        records,
        key=lambda x: float(x.get("score", 0)),
        reverse=True
    )[:5]

    total_score = sum(
        float(item.get("score", 0))
        for item in selected
    )

    if total_score == 0:
        return {
            "results": [],
            "portfolio_dates": [],
            "portfolio_values": []
        }

    results = []
    portfolio_map = {}

    for item in selected:
        stock_code = str(item["code"]).replace(".0", "")

        df = get_backtest_data(
            stock_code,
            start_date,
            holding_days
        )

        if df is None:
            continue

        start_price = df.iloc[0]["收盤價"]

        stop_loss_rate = float(item.get("stop_loss_rate", 8))
        take_profit_rate = float(item.get("take_profit_rate", 15))

        stop_loss_price = start_price * (1 - stop_loss_rate / 100)
        take_profit_price = start_price * (1 + take_profit_rate / 100)

        exit_price = df.iloc[-1]["收盤價"]
        exit_date = df.iloc[-1]["日期"]
        exit_reason = "持有到期"

        max_price = df["收盤價"].max()
        min_price = df["收盤價"].min()

        max_profit_rate = (max_price - start_price) / start_price * 100
        max_loss_rate = (min_price - start_price) / start_price * 100

        stop_loss_triggered = False
        take_profit_triggered = False

        for _, row in df.iterrows():
            price = row["收盤價"]

            if price <= stop_loss_price:
                exit_price = price
                exit_date = row["日期"]
                exit_reason = "觸發停損"
                stop_loss_triggered = True
                break

            if price >= take_profit_price:
                exit_price = price
                exit_date = row["日期"]
                exit_reason = "觸發停利"
                take_profit_triggered = True
                break

        return_rate = (exit_price - start_price) / start_price

        score = float(item.get("score", 0))
        ratio = score / total_score

        invest_amount = capital * ratio
        final_amount = invest_amount * (1 + return_rate)
        profit = final_amount - invest_amount

        daily_values = []

        for _, row in df.iterrows():
            date_text = row["日期"].strftime("%Y-%m-%d")
            price = row["收盤價"]

            value = invest_amount * (price / start_price)
            daily_values.append(round(value, 0))

            if date_text not in portfolio_map:
                portfolio_map[date_text] = 0

            portfolio_map[date_text] += value

        result = {
            "equity_point": round(final_amount, 0),
            "code": stock_code,
            "name": item["name"],
            "score": score,
            "ratio": round(ratio * 100, 2),
            "start_price": round(start_price, 2),
            "end_price": round(exit_price, 2),
            "exit_price": round(exit_price, 2),
            "exit_date": exit_date.strftime("%Y-%m-%d"),
            "exit_reason": exit_reason,
            "stop_loss_price": round(stop_loss_price, 2),
            "take_profit_price": round(take_profit_price, 2),
            "stop_loss_triggered": stop_loss_triggered,
            "take_profit_triggered": take_profit_triggered,
            "max_profit_rate": round(max_profit_rate, 2),
            "max_loss_rate": round(max_loss_rate, 2),
            "invest_amount": round(invest_amount, 0),
            "return_rate": round(return_rate * 100, 2),
            "final_amount": round(final_amount, 0),
            "profit": round(profit, 0),
            "holding_days": holding_days,
            "dates": df["日期"].dt.strftime("%Y-%m-%d").tolist(),
            "prices": df["收盤價"].tolist(),
            "daily_values": daily_values
        }

        results.append(result)

    portfolio_dates = sorted(portfolio_map.keys())

    portfolio_values = [
        round(portfolio_map[date], 0)
        for date in portfolio_dates
    ]

    return {
        "results": results,
        "portfolio_dates": portfolio_dates,
        "portfolio_values": portfolio_values
    }