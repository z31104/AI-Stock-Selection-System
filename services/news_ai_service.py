def generate_news_summary(news_result):

    score = news_result["news_score"]

    if score >= 5:
        sentiment = "偏多"
    elif score >= 2:
        sentiment = "小幅偏多"
    elif score >= 0:
        sentiment = "中性"
    else:
        sentiment = "偏空"

    return f"""
新聞情緒：{sentiment}

新聞熱度：{news_result['news_heat']}

主要題材：
{news_result['news_topics']}

正向關鍵字：
{news_result['positive_keywords']}

負向關鍵字：
{news_result['negative_keywords']}

投資建議：
{news_result['news_advice']}
"""