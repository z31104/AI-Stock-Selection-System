def run_simulation(records, capital):
    if len(records) == 0:
        return []

    records = sorted(
        records,
        key=lambda x: float(x.get("score", 0)),
        reverse=True
    )[:5]

    total_score = sum(float(item.get("score", 0)) for item in records)

    results = []

    for item in records:
        score = float(item.get("score", 0))
        price = float(item.get("price", 0))

        ratio = score / total_score
        amount = capital * ratio

        stop_loss_price = price * 0.92
        take_profit_price = price * 1.15

        results.append({
            "code": str(item["code"]).replace(".0", ""),
            "name": item["name"],
            "score": score,
            "price": price,
            "ratio": round(ratio * 100, 2),
            "amount": round(amount, 0),
            "stop_loss_price": round(stop_loss_price, 2),
            "take_profit_price": round(take_profit_price, 2)
        })

    return results