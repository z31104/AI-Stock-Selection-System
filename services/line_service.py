import os
import requests


def send_line_message(user_id, message):
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    return response.status_code, response.text