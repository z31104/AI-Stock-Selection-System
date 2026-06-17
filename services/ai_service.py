def generate_ai_analysis(result):
    analysis = []

    analysis.append(f"【{result['code']} {result['name']} AI 綜合分析】")
    analysis.append("")
    analysis.append(f"目前收盤價：{result['price']} 元")
    analysis.append(
        f"技術分數：{result['tech_score']} 分｜"
        f"新聞分數：{result['news_score']} 分｜"
        f"綜合分數：{result['final_score']} 分"
    )

    analysis.append("")
    analysis.append("一、技術面分析")

    if result["ma5"] > result["ma20"]:
        analysis.append("1. MA5 高於 MA20，短線均線結構偏多。")
    else:
        analysis.append("1. MA5 低於 MA20，短線均線結構偏弱。")

    if result["price"] > result["ma5"]:
        analysis.append("2. 股價站上 MA5，代表短線買盤仍有支撐。")
    else:
        analysis.append("2. 股價跌破 MA5，短線需要留意轉弱風險。")

    if result["rsi"] >= 70:
        analysis.append(f"3. RSI 為 {result['rsi']}，已接近過熱區，追價風險偏高。")
    elif result["rsi"] <= 30:
        analysis.append(f"3. RSI 為 {result['rsi']}，位於偏低區，有技術反彈機會。")
    else:
        analysis.append(f"3. RSI 為 {result['rsi']}，位於合理區間。")

    if result["k"] > result["d"]:
        analysis.append("4. KD 指標 K 值高於 D 值，短線動能偏多。")
    else:
        analysis.append("4. KD 指標 K 值低於 D 值，短線動能偏弱。")

    analysis.append("")
    analysis.append("二、新聞面分析")
    analysis.append(f"1. 新聞趨勢：{result['news_trend']}")
    analysis.append(f"2. 新聞熱度：{result['news_heat']}")
    analysis.append(f"3. 近期題材：{result['news_topics']}")
    analysis.append(f"4. 正向關鍵字：{result['positive_keywords']}")
    analysis.append(f"5. 負向關鍵字：{result['negative_keywords']}")
    analysis.append(f"6. 新聞建議：{result['news_advice']}")

    analysis.append("")
    analysis.append("三、風險控管")

    analysis.append(
        f"1. 建議停損價：約 {result['stop_loss_price']} 元 "
        f"（-{result['stop_loss_rate']}%）"
    )

    analysis.append(
        f"2. 建議停利價：約 {result['take_profit_price']} 元 "
        f"（+{result['take_profit_rate']}%）"
    )

    analysis.append(f"3. 系統風險等級：{result['risk_level']}")
    analysis.append(f"4. 風險說明：{result['risk_advice']}")

    analysis.append("")
    analysis.append("四、綜合操作建議")

    final_score = result["final_score"]

    if final_score >= 10:
        advice = (
            "整體訊號偏強，技術面與新聞面皆有支撐，"
            "可列入優先觀察名單，但仍建議分批進場，避免一次重押。"
        )
    elif final_score >= 6:
        advice = (
            "整體屬於中性偏多，若後續股價能維持在 MA5 或 MA20 之上，"
            "可考慮小部位分批布局。"
        )
    elif final_score >= 3:
        advice = (
            "整體訊號普通，建議先觀察量能與新聞是否延續，"
            "不建議過度追高。"
        )
    else:
        advice = (
            "目前整體訊號偏弱，技術面或新聞面尚未形成明確優勢，"
            "建議保守觀察。"
        )

    analysis.append(advice)

    analysis.append("")
    analysis.append("※ 本分析為系統依技術指標與新聞關鍵字產生，僅供投資研究與作品展示使用。")

    return "\n".join(analysis)