def get_ai_pick(records, capital, risk_type="medium"):
    # 排除沒有分數的資料
    valid_records = []

    for item in records:
        score = float(item.get("score", 0))

        if score > 0:
            item["score"] = score
            valid_records.append(item)

    if len(valid_records) == 0:
        return {
            "stocks": [],
            "report": "目前沒有可推薦的股票資料。請先查詢幾支股票。"
        }

    # 同一支股票只保留最新一筆
    latest_map = {}

    for item in valid_records:
        code = str(item.get("code", "")).replace(".0", "")
        item["code"] = code
        latest_map[code] = item

    valid_records = list(latest_map.values())

    # 依綜合分數排序
    valid_records = sorted(
        valid_records,
        key=lambda x: float(x.get("score", 0)),
        reverse=True
    )

    # 依風險類型決定推薦數量
    if risk_type == "low":
        selected = valid_records[:3]
        risk_name = "保守型"
    elif risk_type == "high":
        selected = valid_records[:8]
        risk_name = "積極型"
    else:
        selected = valid_records[:5]
        risk_name = "穩健型"

    total_score = sum(
        float(item.get("score", 0))
        for item in selected
    )

    if total_score == 0:
        return {
            "stocks": [],
            "report": "目前分數不足，無法產生推薦。"
        }

    for item in selected:
        score = float(item.get("score", 0))
        ratio = score / total_score

        item["ratio"] = round(ratio * 100, 2)
        item["amount"] = round(capital * ratio, 0)

        reason = []

        if score >= 10:
            reason.append("綜合分數高")

        if float(item.get("news_score", 0)) >= 3:
            reason.append("新聞偏正向")

        if item.get("industry", "未分類") != "未分類":
            reason.append("具產業分類")

        if item.get("risk_level", "") in ["中低風險", "中風險"]:
            reason.append("風險可控")

        if len(reason) == 0:
            reason.append("符合基本篩選條件")

        item["ai_reason"] = "、".join(reason)

    # 產生 AI 投資報告
    report = []

    report.append(f"投資風格：{risk_name}")
    report.append(f"投入本金：{round(capital, 0)} 元")
    report.append(f"推薦股票數量：{len(selected)} 檔")
    report.append("")
    report.append("推薦配置：")

    for item in selected:
        report.append(
            f"- {item['code']} {item['name']}："
            f"配置 {item['ratio']}%，約 {item['amount']} 元。"
        )

    report.append("")
    report.append(
        "系統說明：本次推薦依照綜合分數、新聞分數、風險等級與產業分類進行排序。"
    )

    if risk_type == "low":
        report.append(
            "保守型策略會選擇較少檔股票，降低波動，適合風險承受度較低的投資人。"
        )
    elif risk_type == "high":
        report.append(
            "積極型策略會推薦較多檔股票，追求較高機會，但波動也可能較大。"
        )
    else:
        report.append(
            "穩健型策略會在分散配置與成長機會之間取得平衡。"
        )

    report.append(
        "建議搭配停損停利設定與現金保留比例，避免單次投入造成風險過度集中。"
    )

    report_text = "\n".join(report)

    return {
        "stocks": selected,
        "report": report_text
    }