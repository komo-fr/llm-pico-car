from typing import Dict, List

import config
import requests
from langsmith import traceable


def send_health_check():
    """
    picoカーにヘルスチェックを送る
    """
    response = requests.get(f"{config.BASE_URL}/health")
    return response.text


@traceable(name="send_commands")
def send_commands(commands: List[Dict[str, str | int]]):
    """
    picoカーにコマンドを送る
    """
    response = requests.post(f"{config.BASE_URL}/command", json=commands)
    return response.json()


@traceable(name="send_status")
def send_status(status: str):
    """
    picoカーにステータスを送る
    """
    # response = requests.post(f"{BASE_URL}/status", data=status.encode())
    headers = {"Content-Type": "text/plain"}
    response = requests.post(
        f"{config.BASE_URL}/status", data=status.encode(), headers=headers
    )
    return response.json()


@traceable(name="set_settings")
def set_settings(settings: Dict[str, str | int]):
    """
    picoカーに設定を送る
    """
    response = requests.post(f"{config.BASE_URL}/settings", json=settings)
    return response.json()


@traceable(name="get_settings")
def get_settings():
    """
    picoカーの設定を取得する
    """
    response = requests.get(f"{config.BASE_URL}/settings")
    print(response)
    return response.json()


@traceable(name="reset_settings")
def reset_settings():
    """
    picoカーの設定をリセットする
    """
    response = requests.post(f"{config.BASE_URL}/settings/reset")
    return response.json()
