# 環境構築

このプロジェクトは2つのサーバで構成されています。

| サーバ | 実行環境 | 役割 |
|----------------|----------|------|
| **💻 Pico Controllerサーバ** | PC (Python 3.x) | Gradio UIで入力を受け、コマンドをPico Carサーバへ送信 |
| **🚜 Pico Carサーバ** | Raspberry Pi Pico WH (MicroPython) | コマンドを受け取り車体を制御 |

Mockモードの場合は、両方ともPC上で動かせます。

## 💻 Pico Controllerサーバの環境構築
1. Pico Controllerサーバを動かすPCで、以下のコマンドを実行します。

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install openai-whisper==20250625
```

2. 環境変数に以下を設定します。
```
# OpenAIのAPIキーを取得して設定する
OPENAI_API_KEY={OpenAIのAPIキー}

# Mock（開発・テスト）用のAPIサーバURL
BASE_URL_MOCK=http://localhost:5001/

# 実機（Raspberry Pi Pico）用のAPIサーバURL
BASE_URL_REAL=http://192.168.11.49:5001/
```

3. （必要に応じて実施）LangSmithでログを取りたい場合は、環境変数に以下を設定します。
```
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY={LangSmithのAPIキー}
LANGSMITH_PROJECT="pico-car"
```

## 🚜 Pico Carサーバの環境構築
**PCなどのCPython環境でmockモードを使って動かす** 場合は、前述の「Pico Controllerサーバ」と同じvenvで動きます。

**Raspberry Pi Picoの車体キット上のMicroPythonで動かす** 場合は、次の手順を実施してください。

1. Kitronik社が公開しているキットのチュートリアルの手順にしたがってファイル等を配置し、キットが動く状態にします。
    - [Online Tutorial \- Autonomous Robotics Platform for Pico \- Using the Mo – Kitronik Ltd](https://kitronik.co.uk/blogs/resources/online-tutorial-autonomous-robotics-platform-for-pico-motors)
2. MicrodotをRaspberry Pi Picoにインストールします。
    - [Installation — Microdot documentation](https://microdot.readthedocs.io/en/latest/intro.html#micropython-installation)
    - 具体的には、Pico内に `microdot` フォルダを作成し、下記ファイルを手動でコピーする
        - `__init__.py`
        - `microdot.py`
3. 本リポジトリの `pico` フォルダ配下のファイルを、Pico内にコピーします。

**最終的に、Raspberry Pi Pico内は下記のようなフォルダ構成になります。**

```
- microdot
|    |- __init__.py
|    |- microdot.py
|
|- main.py
|- PicoAutonomousRobotics.py
|- pico_car.py
|- settings.py
|- wifi_connector.py
```

4. `settings.py` の `SSID` / `PASSWORD` を設定します。`192.168.11.49` は、前述の環境変数の `BASE_URL_REAL` にあわせてください。

```
SSID = "..."  # WiFiのSSIDを設定する
PASSWORD = "..."  # WiFiのパスワードを設定する
IP_ADDRESS = "192.168.11.49"  # 前述の環境変数のBASE_URL_REALに合わせる
```
