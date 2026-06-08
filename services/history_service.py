import os
import pandas as pd


def clear_history():
    file_path = "data/history.csv"

    if os.path.isfile(file_path):
        os.remove(file_path)


def save_history(result):
    os.makedirs("data", exist_ok=True)

    file_path = "data/history.csv"

    record = pd.DataFrame([result])

    file_exists = os.path.isfile(file_path)

    record.to_csv(
        file_path,
        mode="a",
        index=False,
        header=not file_exists,
        encoding="utf-8-sig"
    )


def get_history():
    file_path = "data/history.csv"

    if os.path.isfile(file_path):
        df = pd.read_csv(
            file_path,
            encoding="utf-8-sig",
            on_bad_lines="skip"
        )
        return df.to_dict("records")

    return []


def get_latest_history():
    records = get_history()

    latest_map = {}

    for item in records:
        code = str(item.get("code", "")).replace(".0", "")

        if code == "" or code == "nan":
            continue

        item["code"] = code
        latest_map[code] = item

    return list(latest_map.values())