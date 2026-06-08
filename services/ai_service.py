def generate_ai_analysis(result):
    analysis = []

    analysis.append(
        f"{result['code']} {result['name']} "
        f"目前收盤價為 {result['price']} 元。"
    )

    analysis.append(
        f"技術分數 {result['tech_score']} 分，"
        f"新聞分數 {result['news_score']} 分，"
        f"綜合分數 {result['final_score']} 分。"
    )

    # 技術面
    if result["ma5"] > result["ma20"]:
        tech_trend = "短線偏多"
        analysis.append(
            "MA5 高於 MA20，代表短期均線仍維持強勢結構。"
        )
    else:
        tech_trend = "短線偏弱"
        analysis.append(
            "MA5 低於 MA20，代表短期技術面偏保守。"
        )

    if result["price"] > result["ma5"]:
        analysis.append(
            "目前股價仍站上 MA5，短線買盤仍具有支撐。"
        )
    else:
        analysis.append(
            "股價跌破 MA5，需留意短線轉弱風險。"
        )

    if result["rsi"] >= 70:
        analysis.append(
            "RSI 已接近過熱區，追價風險偏高。"
        )
    elif result["rsi"] <= 30:
        analysis.append(
            "RSI 偏低，短線有技術反彈機會。"
        )
    else:
        analysis.append(
            "RSI 位於合理區間，市場情緒中性。"
        )

    if result["k"] > result["d"]:
        analysis.append(
            "KD 呈現黃金交叉型態，短線偏多。"
        )
    else:
        analysis.append(
            "KD 呈現死亡交叉或轉弱訊號。"
        )

    # 新聞面
    analysis.append(
        f"新聞面判斷：{result['news_trend']}。"
    )

    analysis.append(
        f"近期題材：{result['news_topics']}。"
    )

    analysis.append(
        f"新聞熱度：{result['news_heat']}。"
    )

    # 綜合判斷
    final_score = result["final_score"]

    if final_score >= 8:
        advice = (
            "整體偏強，可列入優先觀察，"
            "若成交量同步放大可考慮分批布局。"
        )
    elif final_score >= 5:
        advice = (
            "整體中性偏多，建議等待技術面確認後再進場。"
        )
    else:
        advice = (
            "目前訊號偏弱，不建議積極追價。"
        )

    analysis.append(advice)

    analysis.append(
        f"建議停損價位約 "
        f"{result['stop_loss_price']} 元，"
        f"停利價位約 "
        f"{result['take_profit_price']} 元。"
    )

    analysis.append(
        f"系統風險判斷：{result['risk_level']}。"
    )

    return "\n".join(analysis)