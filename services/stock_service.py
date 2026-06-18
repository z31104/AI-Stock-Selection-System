import requests
import pandas as pd
import urllib3
import redis
import json
import os

from datetime import datetime

urllib3.disable_warnings()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def get_stock_data(stock_code):
    cache_key = f"stock:{stock_code}"

    try:
        cached_data = redis_client.get(cache_key)
    except Exception:
        cached_data = None

    if cached_data:
        print(f"Redis Cache Hit: {stock_code}")
        cache = json.loads(cached_data)
        df = pd.DataFrame(cache["df"])
        return {
            "stock_name": cache["stock_name"],
            "df": df
        }, None
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY"

    today = datetime.now()

    month_list = []

    for i in range(3):
        month = today.month - i
        year = today.year

        if month <= 0:
            month += 12
            year -= 1

        month_list.append(f"{year}{month:02d}01")

    all_dfs = []
    stock_name = ""

    for date in month_list:
        params = {
            "response": "json",
            "date": date,
            "stockNo": stock_code
        }

        response = requests.get(url, params=params, verify=False)
        data = response.json()

        if "data" not in data or len(data["data"]) == 0:
            continue

        title = data.get("title", "")
        parts = title.split()

        if len(parts) >= 3:
            stock_name = parts[2]
        else:
            stock_name = title

        df = pd.DataFrame(data["data"], columns=data["fields"])

        df["日期"] = df["日期"].apply(
            lambda x: str(int(x.split("/")[0]) + 1911) + "-" + x.split("/")[1] + "-" + x.split("/")[2]
        )

        number_columns = ["開盤價", "最高價", "最低價", "收盤價", "成交股數"]

        for col in number_columns:
            df[col] = df[col].str.replace(",", "").astype(float)

        all_dfs.append(df)

    if len(all_dfs) == 0:
         return None, f"查無 {stock_code} 的股票資料，請確認是否為上市股票代號"

    final_df = pd.concat(all_dfs)
    final_df = final_df.drop_duplicates(subset=["日期"])
    final_df = final_df.sort_values("日期")

    cache_data = {
        "stock_name": stock_name,
        "df": final_df.to_dict("records")
    }

    redis_client.setex(
        cache_key,
        86400,
        json.dumps(cache_data, ensure_ascii=False)
    )

    print(f"Redis Cache Save: {stock_code}")

    return {
        "stock_name": stock_name,
        "df": final_df
    }, None