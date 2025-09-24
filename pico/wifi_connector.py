from time import sleep

import network


def connect_to_wifi(ssid, password, ip_address=None, max_retry=10):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    STATUS_MAP = {
        network.STAT_IDLE: "無接続、無アクティビティ",
        network.STAT_CONNECTING: "接続中",
        network.STAT_WRONG_PASSWORD: "パスワード不正により失敗",
        network.STAT_NO_AP_FOUND: "アクセスポイントが応答しないため失敗",
        network.STAT_CONNECT_FAIL: "その他の問題により失敗",
        network.STAT_GOT_IP: "接続成功",
    }
    desc = "\n".join([f"- {status}: {desc}" for status, desc in STATUS_MAP.items()])
    print(desc)

    for i in range(max_retry):
        status = wlan.status()
        if status < 0 or status == network.STAT_GOT_IP:
            break
        print(f"[{i + 1}/{max_retry}] ネットワーク接続中...（{status=}）")
        sleep(1)

    if status == network.STAT_GOT_IP:
        wlan_status = wlan.ifconfig()
        # IPアドレスを固定する
        wlan.ifconfig((ip_address, wlan_status[1], wlan_status[2], wlan_status[3]))
        print("✅ 接続に成功")
        print("IPアドレス:", ip_address)
    else:
        raise RuntimeError(
            f"ネットワークの接続に失敗しました（{status}: {STATUS_MAP.get(status, '不明なエラー')}）"
        )
