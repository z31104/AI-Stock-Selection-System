from flask import Flask, render_template, request

from services.stock_service import get_stock_data
from services.indicator_service import add_indicators
from services.score_service import calculate_score
from services.chart_service import create_stock_chart
from services.history_service import (
    save_history,
    get_history,
    get_latest_history,
    clear_history
)
from services.portfolio_service import allocate_portfolio
from services.ai_service import generate_ai_analysis
from services.risk_service import get_risk_advice
from services.industry_service import get_industry
from services.backtest_service import run_real_backtest
from services.simulation_service import run_simulation
from services.news_service import analyze_news_trend
from services.ai_pick_service import get_ai_pick

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        stock_code = request.form["stock"].strip()
        if stock_code == "":
            error = "請輸入股票代號"
            return render_template("index.html", result=result, error=error)

        if not stock_code.isdigit():
            error = "股票代號只能輸入數字"
            return render_template("index.html", result=result, error=error)
        min_score = int(request.form.get("min_score", 0))
        max_rsi = float(request.form.get("max_rsi", 70))
        above_ma5 = "above_ma5" in request.form
        stop_loss_rate = float(request.form.get("stop_loss_rate", 8))
        take_profit_rate = float(request.form.get("take_profit_rate", 15))

        stock_data, error = get_stock_data(stock_code)
        if error:
            return render_template("index.html", result=result, error=error)

        if stock_data:
            df = stock_data["df"]
            df = add_indicators(df)

            if len(df) == 0:
                error = "資料不足，無法計算技術指標"
            else:
                latest = df.iloc[-1]

                tech_score, suggestion = calculate_score(latest)
                industry = get_industry(stock_code)

                is_valid = True

                if tech_score < min_score:
                    is_valid = False

                if latest["RSI"] > max_rsi:
                    is_valid = False

                if above_ma5 and latest["收盤價"] < latest["MA5"]:
                    is_valid = False

                if is_valid:
                    chart_file = create_stock_chart(df, stock_code)

                    news_result = analyze_news_trend(
                        stock_code,
                        stock_data["stock_name"]
                    )

                    final_score = tech_score + news_result["news_score"]

                    result = {
                        "code": stock_code,
                        "name": stock_data["stock_name"],
                        "price": latest["收盤價"],
                        "industry": industry,
                        "volume": int(latest["成交股數"]),
                        "ma5": round(latest["MA5"], 2),
                        "ma20": round(latest["MA20"], 2),
                        "rsi": round(latest["RSI"], 2),
                        "k": round(latest["K"], 2),
                        "d": round(latest["D"], 2),
                        "volume_ma5": int(latest["成交量MA5"]),

                        "tech_score": tech_score,
                        "news_score": news_result["news_score"],
                        "final_score": final_score,
                        "score": final_score,

                        "suggestion": suggestion,
                        "chart_file": chart_file,

                        "news_trend": news_result["news_trend"],
                        "news_list": news_result["news_list"],
                        "news_titles": " | ".join(
                            [news["title"] for news in news_result["news_list"]]
                        ),

                        "news_heat": news_result["news_heat"],
                        "news_topics": news_result["news_topics"],
                        "positive_keywords": news_result["positive_keywords"],
                        "negative_keywords": news_result["negative_keywords"],
                        "news_advice": news_result["news_advice"]
                    }

                    risk_advice = get_risk_advice(
                        result,
                        stop_loss_rate,
                        take_profit_rate
                    )
                    result.update(risk_advice)

                    ai_analysis = generate_ai_analysis(result)
                    result["ai_analysis"] = ai_analysis

                    save_history(result)

                else:
                    error = "不符合選股條件"

    return render_template(
        "index.html",
        result=result,
        error=error
    )


@app.route("/history")
def history():
    records = get_history()
    return render_template("history.html", records=records)


@app.route("/clear_history")
def clear_history_route():
    clear_history()
    return render_template("history.html", records=[])


@app.route("/ranking")
def ranking():
    records = get_latest_history()

    records = sorted(
        records,
        key=lambda x: float(x.get("score", 0)),
        reverse=True
    )

    return render_template(
        "ranking.html",
        records=records
    )


@app.route("/compare")
def compare():
    records = get_latest_history()
    return render_template("compare.html", records=records)


@app.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    portfolio_data = None
    capital = None

    if request.method == "POST":
        capital = float(request.form.get("capital", 1000000))
        cash_ratio = float(request.form.get("cash_ratio", 10))
        stop_loss_rate = float(request.form.get("stop_loss_rate", 8))
        take_profit_rate = float(request.form.get("take_profit_rate", 15))
        buy_mode = request.form.get("buy_mode", "odd")

        invest_capital = capital * (1 - cash_ratio / 100)
        cash_amount = capital * (cash_ratio / 100)

        records = get_latest_history()

        portfolio_data = allocate_portfolio(
            records,
            invest_capital,
            stop_loss_rate,
            take_profit_rate,
            buy_mode
        )

        portfolio_data["cash_ratio"] = cash_ratio
        portfolio_data["cash_amount"] = round(cash_amount, 0)
        portfolio_data["invest_capital"] = round(invest_capital, 0)
        portfolio_data["advice"] = (
            f"本次總本金為 {round(capital, 0)} 元，"
            f"保留現金 {cash_ratio}% ，約 {round(cash_amount, 0)} 元，"
            f"實際投入金額約 {round(invest_capital, 0)} 元。"
            "系統依照綜合分數、新聞趨勢與產業分散進行配置，"
            "建議分批進場，並依照停損停利價格執行風險控管。"
        )

    return render_template(
        "portfolio.html",
        portfolio_data=portfolio_data,
        capital=capital
    )


@app.route("/backtest", methods=["GET", "POST"])
def backtest():
    results = None
    total_profit = None
    capital = None
    start_date = None
    holding_days = 30
    message = None

    if request.method == "POST":
        capital = float(request.form.get("capital", 1000000))
        start_date = request.form.get("start_date", "2025-04-01")
        holding_days = int(request.form.get("holding_days", 30))

        records = get_latest_history()

        results = run_real_backtest(
            records,
            capital,
            start_date,
            holding_days
        )

        if len(results) == 0:
            message = "沒有回測結果，請換日期試試"
            total_profit = 0
        else:
            total_profit = sum(item["profit"] for item in results)

    return render_template(
        "backtest.html",
        results=results,
        total_profit=total_profit,
        capital=capital,
        start_date=start_date,
        holding_days=holding_days,
        message=message
    )


@app.route("/simulation", methods=["GET", "POST"])
def simulation():
    results = None
    capital = None

    if request.method == "POST":
        capital = float(request.form.get("capital", 1000000))

        records = get_latest_history()
        results = run_simulation(records, capital)

    return render_template(
        "simulation.html",
        results=results,
        capital=capital
    )


@app.route("/ai_pick", methods=["GET", "POST"])
def ai_pick():
    ai_result = None
    capital = None
    pdf_file = None

    if request.method == "POST":
        risk_type = request.form.get("risk_type", "medium")
        capital = float(request.form.get("capital", 1000000))

        records = get_latest_history()

        ai_result = get_ai_pick(
            records,
            capital,
            risk_type
        )

    return render_template(
        "ai_pick.html",
        ai_result=ai_result,
        capital=capital,
        pdf_file=pdf_file
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)