def add_indicators(df):
    df = df.copy()

    # 移動平均線
    df["MA5"] = df["收盤價"].rolling(5).mean()
    df["MA20"] = df["收盤價"].rolling(20).mean()

    # 成交量 5 日均量
    df["成交量MA5"] = df["成交股數"].rolling(5).mean()

    # RSI
    df["漲跌"] = df["收盤價"].diff()
    df["漲"] = df["漲跌"].apply(lambda x: x if x > 0 else 0)
    df["跌"] = df["漲跌"].apply(lambda x: -x if x < 0 else 0)

    df["平均漲"] = df["漲"].rolling(14).mean()
    df["平均跌"] = df["跌"].rolling(14).mean()

    df["RSI"] = 100 - (100 / (1 + df["平均漲"] / df["平均跌"]))

    # KD
    low_9 = df["最低價"].rolling(9).min()
    high_9 = df["最高價"].rolling(9).max()

    df["RSV"] = (df["收盤價"] - low_9) / (high_9 - low_9) * 100
    df["K"] = df["RSV"].ewm(com=2).mean()
    df["D"] = df["K"].ewm(com=2).mean()

    df = df.dropna()

    return df