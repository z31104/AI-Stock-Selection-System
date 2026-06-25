import os
import requests
from dotenv import load_dotenv

load_dotenv()


def local_rule_analysis(stock_data):
    name = stock_data.get("name", "")
    code = stock_data.get("code", "")
    close = stock_data.get("close", "")
    ma5 = stock_data.get("ma5", "")
    ma20 = stock_data.get("ma20", "")
    rsi = stock_data.get("rsi", "")
    score = stock_data.get("score", "")

    return f"""
【本機規則分析】
{name}（{code}）目前收盤價 {close}

技術面：
MA5：{ma5}
MA20：{ma20}
RSI：{rsi}
技術分數：{score}

提醒：
此分析僅供參考，不保證獲利。
"""


def generate_gemini_analysis(stock_data):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return local_rule_analysis(stock_data)

    prompt = f"""
你是一位台股投資分析助理，請根據以下資料產生簡短股票分析。

股票名稱：{stock_data.get("name")}
股票代號：{stock_data.get("code")}
收盤價：{stock_data.get("close")}
MA5：{stock_data.get("ma5")}
MA20：{stock_data.get("ma20")}
RSI：{stock_data.get("rsi")}
K值：{stock_data.get("k")}
D值：{stock_data.get("d")}
技術分數：{stock_data.get("score")}

請用繁體中文回答，格式如下：
1. 技術面分析
2. 風險提醒
3. 操作建議

不要保證獲利。
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        data = response.json()

        if response.status_code != 200:
            error_code = data.get("error", {}).get("code")      
            error_status = data.get("error", {}).get("status")

            if error_code == 429 or error_status == "RESOURCE_EXHAUSTED":
                return local_rule_analysis(stock_data) + "\n\n⚠️ Gemini AI 額度不足，已改用本機規則分析。"

            return local_rule_analysis(stock_data) + "\n\n⚠️ Gemini AI 暫時無法使用，已改用本機規則分析。"

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception:
        return local_rule_analysis(stock_data) + "\n\n⚠️ Gemini AI 連線失敗，已改用本機規則分析。"  