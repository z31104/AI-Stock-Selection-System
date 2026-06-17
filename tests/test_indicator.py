from services.indicator_service import add_indicators
import pandas as pd


def test_indicator_columns():

    df = pd.DataFrame({
        "收盤價": [
            10,11,12,13,14,
            15,16,17,18,19,
            20,21,22,23,24,
            25,26,27,28,29
        ],
        "最高價": [
            11,12,13,14,15,
            16,17,18,19,20,
            21,22,23,24,25,
            26,27,28,29,30
        ],
        "最低價": [
            9,10,11,12,13,
            14,15,16,17,18,
            19,20,21,22,23,
            24,25,26,27,28
        ],
        "成交股數": [
            1000,1100,1200,1300,1400,
            1500,1600,1700,1800,1900,
            2000,2100,2200,2300,2400,
            2500,2600,2700,2800,2900
        ]
    })

    result = add_indicators(df)

    assert "MA5" in result.columns
    assert "MA20" in result.columns
    assert "RSI" in result.columns
    assert "K" in result.columns
    assert "D" in result.columns
    assert "成交量MA5" in result.columns