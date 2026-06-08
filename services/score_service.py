def calculate_score(latest):

    score = 0

    # 均線
    if latest["MA5"] > latest["MA20"]:
        score += 2

    # 站上 MA5
    if latest["收盤價"] > latest["MA5"]:
        score += 2

    # RSI
    if 40 <= latest["RSI"] <= 70:
        score += 2

    # KD
    if latest["K"] > latest["D"]:
        score += 2

    # 量價
    if latest["成交股數"] > latest["成交量MA5"]:
        score += 2

    # 強勢突破
    if latest["收盤價"] > latest["最高價"] * 0.98:
        score += 2

    # RSI 強勢區
    if latest["RSI"] > 50:
        score += 1

    # KD 超強
    if latest["K"] > 80:
        score += 1

    # 量能暴增
    if latest["成交股數"] > latest["成交量MA5"] * 1.5:
        score += 1

    if score >= 12:
        suggestion = "強勢股，可優先觀察"

    elif score >= 8:
        suggestion = "中期偏多"

    elif score >= 5:
        suggestion = "中性偏多"

    else:
        suggestion = "偏弱"

    return score, suggestion