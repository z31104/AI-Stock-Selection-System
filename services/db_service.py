import os
import sqlite3


DB_PATH = "data/stock.db"


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            code TEXT,
            name TEXT,
            industry TEXT,
            price REAL,
            ma5 REAL,
            ma20 REAL,
            rsi REAL,
            k REAL,
            d REAL,
            volume REAL,
            volume_ma5 REAL,
            tech_score REAL,
            news_score REAL,
            final_score REAL,
            score REAL,
            suggestion TEXT,
            news_trend TEXT,
            news_heat TEXT,
            news_topics TEXT,
            positive_keywords TEXT,
            negative_keywords TEXT,
            news_advice TEXT,
            risk_level TEXT,
            stop_loss_price REAL,
            take_profit_price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("PRAGMA table_info(stock_history)")
    columns = [column[1] for column in cursor.fetchall()]

    if "user_id" not in columns:
        cursor.execute("""
            ALTER TABLE stock_history
            ADD COLUMN user_id INTEGER
        """)

    conn.commit()
    conn.close()


def save_stock(result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO stock_history (
            user_id,
            code,
            name,
            industry,
            price,
            ma5,
            ma20,
            rsi,
            k,
            d,
            volume,
            volume_ma5,
            tech_score,
            news_score,
            final_score,
            score,
            suggestion,
            news_trend,
            news_heat,
            news_topics,
            positive_keywords,
            negative_keywords,
            news_advice,
            risk_level,
            stop_loss_price,
            take_profit_price
        )
        VALUES (
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?
        )
    """, (
        result.get("user_id", None),
        result.get("code", ""),
        result.get("name", ""),
        result.get("industry", ""),
        result.get("price", 0),
        result.get("ma5", 0),
        result.get("ma20", 0),
        result.get("rsi", 0),
        result.get("k", 0),
        result.get("d", 0),
        result.get("volume", 0),
        result.get("volume_ma5", 0),
        result.get("tech_score", 0),
        result.get("news_score", 0),
        result.get("final_score", 0),
        result.get("score", 0),
        result.get("suggestion", ""),
        result.get("news_trend", ""),
        result.get("news_heat", ""),
        result.get("news_topics", ""),
        str(result.get("positive_keywords", "")),
        str(result.get("negative_keywords", "")),
        result.get("news_advice", ""),
        result.get("risk_level", ""),
        result.get("stop_loss_price", 0),
        result.get("take_profit_price", 0)
    ))

    conn.commit()
    conn.close()


def get_all_stocks(user_id=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if user_id:
        cursor.execute("""
            SELECT *
            FROM stock_history
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT *
            FROM stock_history
            ORDER BY id DESC
        """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_latest_stocks(user_id=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if user_id:
        cursor.execute("""
            SELECT *
            FROM stock_history
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT *
            FROM stock_history
            ORDER BY id DESC
        """)

    rows = cursor.fetchall()
    conn.close()

    latest_map = {}

    for row in rows:
        item = dict(row)
        code = str(item.get("code", ""))

        if code not in latest_map:
            latest_map[code] = item

    return list(latest_map.values())