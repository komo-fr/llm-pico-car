import sys
import time

import settings
from microdot import Microdot

# MicroPythonだとargparseが使えないので、sys.argvを使う
settings.USE_MOCK = "--mock" in sys.argv
print(f"mock mode: {settings.USE_MOCK}")

from pico_car import Car, RealCar  # noqa: E402

car = Car() if settings.USE_MOCK else RealCar()
app = Microdot()


def print_exception(e) -> None:
    """MicroPython/CPythonの両方で例外を出力する互換関数"""
    if hasattr(sys, "print_exception"):  # MicroPython用
        sys.print_exception(e)
    else:
        import traceback
        traceback.print_exception(e)


@app.route("stop_all")
async def stop_all(request):
    print("stop_all")
    car.stop_all()
    return {"status": "ok"}


@app.route("/health")
async def check_health(request):
    print("health check!!")
    car.on_mini_led()
    time.sleep(3)
    car.off_mini_led()
    return {"status": "ok"}


@app.before_request
def log_request(request):
    print(f"[REQ] {request.method} {request.path}")
    car.stop_all()


@app.after_request
def log_response(request, response):
    status = getattr(response, "status_code", getattr(response, "status", 200))
    print(f"[RES] {status} {request.method} {request.path}")
    return response


@app.route("/status", methods=["POST"])
async def set_status(request):
    try:
        print(request.body)
        status = request.body.decode().strip()
        print(f"受信ステータス: {status}")
        car.show_status(status)
        return {"status": "ok", "received": status}
    except Exception as e:
        handle_car_error()
        print_exception(e)
        return {"status": "error", "message": str(e)}, 500


@app.route("/settings", methods=["POST"])
async def set_settings(request):
    try:
        car_settings = request.json
        car.set_settings(**car_settings)
        return {"status": "ok", "settings": car.get_settings()}
    except Exception as e:
        print_exception(e)
        return {"status": "error", "message": str(e)}, 500

@app.route("/settings", methods=["GET"])
async def get_settings(request):
    try:
        car_settings = car.get_settings()
        return {"status": "ok", "settings": car_settings}
    except Exception as e:
        print_exception(e)
        return {"status": "error", "message": str(e)}, 500

@app.route("/settings/reset", methods=["POST"])
async def reset_settings(request):
    try:
        car.initialize_settings()
        return {"status": "ok", "settings": car.get_settings()}
    except Exception as e:
        print_exception(e)
        return {"status": "error", "message": str(e)}, 500


@app.route("/command", methods=["POST"])
async def run_commands(request):
    try:
        car.sound_freq(1000, 0.1)
        car.sound_freq(1200, 0.1)
        command_list = request.json
        car.run_commands(command_list)
        return {"status": "ok"}
    except Exception as e:
        handle_car_error()
        print_exception(e)
        return {"status": "error", "message": str(e)}, 500

def handle_car_error():
    car.sound_error()
    car.stop_all()

try:
    if not settings.USE_MOCK:
        from wifi_connector import connect_to_wifi
        car.on_mini_led()
        # Wi-Fiに接続
        connect_to_wifi(settings.SSID,
                        settings.PASSWORD,
                        settings.IP_ADDRESS)
        car.sound_success()
        time.sleep(0.2)
        car.sound_success()
        car.off_mini_led()

    app.run(port=5001)

except Exception as e:
    print("🚨例外発生:", e)
    print_exception(e)
    car.sound_error()
    car.stop_all()
