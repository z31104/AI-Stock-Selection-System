def allocate_portfolio(records, capital, stop_loss_rate=8, take_profit_rate=15, buy_mode="odd", max_industry_ratio=40):
    latest_map = {}

    for item in records:
        code = str(item.get("code", "")).replace(".0", "")
        item["code"] = code
        latest_map[code] = item

    records = list(latest_map.values())
    valid_records = []

    for item in records:
        score = float(item.get("score", 0))

        if score > 0:
            item["score"] = score
            valid_records.append(item)

    if len(valid_records) == 0:
        return {
            "stocks": [],
            "industry_summary": [],
            "summary": "目前沒有可配置的股票資料。"
        }

    valid_records = sorted(
        valid_records,
        key=lambda x: x["score"],
        reverse=True
    )

    selected = []
    industry_count = {}

    max_stocks = 5
    max_same_industry = 2

    for item in valid_records:
        industry = item.get("industry", "未分類")

        if industry_count.get(industry, 0) >= max_same_industry:
            continue

        selected.append(item)
        industry_count[industry] = industry_count.get(industry, 0) + 1

        if len(selected) >= max_stocks:
            break

    total_score = sum(item["score"] for item in selected)

    results = []
    industry_summary_map = {}

    for item in selected:
        ratio = item["score"] / total_score

        # 限制單一股票最高配置 30%
        if ratio > 0.3:
            ratio = 0.3
            
        amount = capital * ratio
        industry = item.get("industry", "未分類")

        price = float(item.get("price", 0))

        shares = 0

        note = ""

        if price > 0:

            if buy_mode == "lot":

                shares = int(amount // (price * 1000)) * 1000

                if shares == 0:
                    shares = int(amount // price)
                    note = "整張不足，自動改零股"

                else:
                    note = "整張模式"

            else:

                shares = int(amount // price)
                note = "零股模式"

        lots = round(shares / 1000, 2)
        actual_amount = round(shares * price, 0)

        stop_loss_price = price * (1 - stop_loss_rate / 100)
        take_profit_price = price * (1 + take_profit_rate / 100)
        reason = []

        if item["score"] >= 10:
            reason.append("技術面強")

        if float(item.get("news_score", 0)) >= 3:
            reason.append("新聞偏正向")

        if industry != "未分類":
            reason.append("產業代表股")

        if len(reason) == 0:
            reason.append("分數符合配置條件")

        reason_text = "、".join(reason)
        note = ""

        if buy_mode == "lot" and shares == 0:
            note = "配置金額不足買一張，建議改用零股"
        else:
            note = "可依設定方式買進"

        results.append({
            "code": item["code"],
            "name": item["name"],
            "industry": industry,
            "score": item["score"],
            "ratio": round(ratio * 100, 2),
            "amount": round(amount, 0),
            "risk_level": item.get("risk_level", "未評估"),
            "stop_loss_price": round(stop_loss_price, 2),
            "take_profit_price": round(take_profit_price, 2),
            "reason": reason_text,
            "price": price,
            "shares": shares,
            "lots": lots,
            "actual_amount": actual_amount,
            "buy_mode": "整張" if buy_mode == "lot" else "零股",
            "note": note,
        })

        if industry not in industry_summary_map:
            industry_summary_map[industry] = 0

        industry_summary_map[industry] += ratio * 100

    industry_summary = []

    for industry, ratio in industry_summary_map.items():
        industry_summary.append({
            "industry": industry,
            "ratio": round(ratio, 2)
        })

    summary = (
        "本次配置依照綜合分數進行資金分配，"
        "分數越高配置比例越高，並限制同產業最多 2 檔，"
        "單一股票最高配置 30%，避免資金過度集中。"
    )

    return {
        "stocks": results,
        "industry_summary": industry_summary,
        "summary": summary
    }