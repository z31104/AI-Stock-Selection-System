def ask_stock_ai(question, records):

    question = question.strip()

    # 查詢分數最高
    if "分數最高" in question or "最高分" in question:

        best = max(
            records,
            key=lambda x: float(x.get("score", 0))
        )

        return f"""
        目前分數最高的是：

    {best.get('code')} {best.get('name')}

    綜合分數：{best.get('score')}
    技術分數：{best.get('tech_score')}
    新聞分數：{best.get('news_score')}

    新聞趨勢：
    {best.get('news_trend')}

    風險等級：
    {best.get('risk_level')}

    建議：
    {best.get('suggestion')}
    """

    # 推薦前三名
    if "前三名" in question:

        top3 = sorted(
            records,
            key=lambda x: float(x.get("score", 0)),
            reverse=True
        )[:3]

        answer = "推薦前三名：\n\n"

        for item in top3:
            answer += (
                f"{item['code']} "
                f"{item['name']} "
                f"分數：{item['score']}\n"
            )

        return answer

    # 查詢個股
    for item in records:

        code = str(item.get("code", ""))
        name = str(item.get("name", ""))

        if code in question or name in question:

            return f"""
股票：{code} {name}

綜合分數：{item.get('score')}
技術分數：{item.get('tech_score')}
新聞分數：{item.get('news_score')}

新聞趨勢：
{item.get('news_trend')}

風險等級：
{item.get('risk_level')}

停損價：
{item.get('stop_loss_price')}

停利價：
{item.get('take_profit_price')}

AI建議：
{item.get('ai_analysis', '暫無分析')}
"""

    return "找不到相關股票資料"