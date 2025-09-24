import os

USE_MOCK = None
BASE_URL = None


def setup(use_mock: bool):
    global USE_MOCK, BASE_URL
    USE_MOCK = use_mock
    BASE_URL = os.getenv("BASE_URL_MOCK" if USE_MOCK else "BASE_URL_REAL")

    if BASE_URL is None:
        raise ValueError("BASE_URLが設定されていません")

    print("[config]")
    print(f"USE_MOCK={USE_MOCK}")
    print(f"BASE_URL={BASE_URL}")
