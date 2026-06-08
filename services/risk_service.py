def get_risk_advice(result, stop_loss_rate=8, take_profit_rate=15):
    price = float(result["price"])
    score = float(result["score"])
    rsi = float(result["rsi"])

    stop_loss_price = price * (1 - stop_loss_rate / 100)
    take_profit_price = price * (1 + take_profit_rate / 100)

    if score >= 4 and rsi < 70:
        risk_level = "中低風險"
        advice = "目前技術面偏強，可依自訂停損停利區間操作。"

    elif score == 3:
        risk_level = "中風險"
        advice = "目前屬於中性偏多，建議停利不要設太遠，並嚴格執行停損。"

    else:
        risk_level = "高風險"
        advice = "目前技術面偏弱，不建議重倉，若進場應降低部位並縮小停損。"

    return {
        "risk_level": risk_level,
        "stop_loss_price": round(stop_loss_price, 2),
        "take_profit_price": round(take_profit_price, 2),
        "stop_loss_rate": stop_loss_rate,
        "take_profit_rate": take_profit_rate,
        "risk_advice": advice
    }