from services.portfolio_service import allocate_portfolio


def test_allocate_portfolio_return_type():

    records = [
        {
            "code": "2330",
            "name": "台積電",
            "score": 10,
            "price": 100,
            "industry": "半導體"
        },
        {
            "code": "2317",
            "name": "鴻海",
            "score": 8,
            "price": 80,
            "industry": "電子"
        }
    ]

    result = allocate_portfolio(
        records=records,
        capital=900000,
        stop_loss_rate=8,
        take_profit_rate=15,
        buy_mode="odd"
    )

    assert isinstance(result, dict)