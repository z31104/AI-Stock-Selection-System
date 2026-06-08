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

    response = requests.get(url, params=params, verify=False)
    data = response.json()

    if "data" not in data or len(data["data"]) == 0:
        return None

    df = pd.DataFrame(data["data"], columns=data["fields"])

    df["日期"] = df["日期"].apply(
        lambda x: str(int(x.split("/")[0]) + 1911) + "-" + x.split("/")[1] + "-" + x.split("/")[2]
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
    if len(records) == 0:
        return []

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
        return []

    results = []

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
        end_price = df.iloc[-1]["收盤價"]

        return_rate = (end_price - start_price) / start_price

        score = float(item.get("score", 0))
        ratio = score / total_score

        invest_amount = capital * ratio
        final_amount = invest_amount * (1 + return_rate)
        profit = final_amount - invest_amount

        result = {
            "code": stock_code,
            "name": item["name"],
            "score": score,
            "ratio": round(ratio * 100, 2),
            "start_price": round(start_price, 2),
            "end_price": round(end_price, 2),
            "invest_amount": round(invest_amount, 0),
            "return_rate": round(return_rate * 100, 2),
            "final_amount": round(final_amount, 0),
            "profit": round(profit, 0),
            "holding_days": holding_days
        }

        results.append(result)

    return results