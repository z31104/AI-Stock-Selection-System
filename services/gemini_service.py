import os
from google import genai


def generate_gemini_analysis(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API Key 尚未設定。"

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        error_msg = str(e)

        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return "Gemini AI 今日免費額度已用完，系統暫時改用原本規則式 AI 分析。"

        return f"Gemini AI 分析失敗：{error_msg}"


if __name__ == "__main__":
    print(
        generate_gemini_analysis(
            "請用繁體中文簡短分析台積電的投資風險。"
        )
    )