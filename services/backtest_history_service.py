import os
import pandas as pd


def save_backtest_history(record):
    os.makedirs("data", exist_ok=True)

    file_path = "data/backtest_history.csv"

    df = pd.DataFrame([record])

    file_exists = os.path.isfile(file_path)

    df.to_csv(
        file_path,
        mode="a",
        index=False,
        header=not file_exists,
        encoding="utf-8-sig"
    )


def get_backtest_history():
    file_path = "data/backtest_history.csv"

    if not os.path.isfile(file_path):
        return []

    df = pd.read_csv(
        file_path,
        encoding="utf-8-sig"
    )

    return df.to_dict("records")

def clear_backtest_history():
    import os

    file_path = "data/backtest_history.csv"

    if os.path.isfile(file_path):
        os.remove(file_path)