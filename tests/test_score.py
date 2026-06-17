from services.score_service import calculate_score


def test_score_return_type():

    sample = {
        "收盤價": 100,
        "MA5": 90,
        "MA20": 80,
        "RSI": 50,
        "K": 70,
        "D": 60,
        "成交股數": 100000,
        "成交量MA5": 80000,
        "最高價": 102
    }

    score, suggestion = calculate_score(sample)

    assert isinstance(score, int)
    assert isinstance(suggestion, str)