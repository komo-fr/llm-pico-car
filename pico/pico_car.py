from time import sleep

from settings import USE_MOCK

if not USE_MOCK:
    from machine import Pin
    from PicoAutonomousRobotics import KitronikPicoRobotBuggy

try:
    import asyncio
except ImportError:
    import uasyncio as asyncio

STATUS_RECORDING_STARTED = "recording_started"
STATUS_AUDIO_TO_TEXT_STARTED = "audio_to_text_started"
STATUS_TEXT_TO_COMMAND_STARTED = "text_to_command_started"
STATUS_IMAGE_TO_TEXT_STARTED = "image_to_text_started"
STATUS_RUN_COMMANDS_STARTED = "run_commands_started"


class Car:
    def __init__(self):
        self.initialize_settings()

    def set_settings(
        self, degree_per_sec=None, cm_per_sec=None, turn_speed=None, drive_speed=None
    ):
        if degree_per_sec is not None:
            self.degree_per_sec = degree_per_sec
        if cm_per_sec is not None:
            self.cm_per_sec = cm_per_sec
        if turn_speed is not None:
            self.turn_speed = turn_speed
        if drive_speed is not None:
            self.drive_speed = drive_speed
        self.status = None

        print("✅ set_settings")
        print(f"{self.degree_per_sec=}")
        print(f"{self.cm_per_sec=}")
        print(f"{self.turn_speed=}")
        print(f"{self.drive_speed=}")

    def initialize_settings(self):
        print("✅ initialize_settings")
        self.degree_per_sec = 6 / 5 * 360
        self.cm_per_sec = 10
        self.turn_speed = 80
        self.drive_speed = 20
        return {
            "degree_per_sec": self.degree_per_sec,
            "cm_per_sec": self.cm_per_sec,
            "turn_speed": self.turn_speed,
            "drive_speed": self.drive_speed,
        }

    def get_settings(self):
        print("✅ get_settings")
        print(f"{self.degree_per_sec=}")
        print(f"{self.cm_per_sec=}")
        print(f"{self.turn_speed=}")
        print(f"{self.drive_speed=}")
        return {
            "degree_per_sec": self.degree_per_sec,
            "cm_per_sec": self.cm_per_sec,
            "turn_speed": self.turn_speed,
            "drive_speed": self.drive_speed,
        }

    def show_status(self, status):
        async def _reaction():
            while self.status == STATUS_AUDIO_TO_TEXT_STARTED:
                self.set_all_led((255, 255, 255), 20)
                await asyncio.sleep(0.2)
                self.clear_all_led()
                await asyncio.sleep(0.2)
            self.clear_all_led()

        async def _thinking():
            while self.status in [
                STATUS_TEXT_TO_COMMAND_STARTED,
                STATUS_IMAGE_TO_TEXT_STARTED,
            ]:
                for i in range(4):
                    self.clear_all_led()
                    self.set_led(i, (255, 255, 255))
                    await asyncio.sleep(0.1)
            self.clear_all_led()

        self.status = status
        if self.status == STATUS_AUDIO_TO_TEXT_STARTED:
            self.sound_freq(800, 0.1)
            asyncio.create_task(_reaction())
        elif self.status in [
            STATUS_TEXT_TO_COMMAND_STARTED,
            STATUS_IMAGE_TO_TEXT_STARTED,
        ]:
            self.sound_freq(900, 0.1)
            asyncio.create_task(_thinking())
        elif self.status == STATUS_RECORDING_STARTED:
            self.set_all_led((255, 255, 255), 10)

    def sound_freq(self, freq, sleep_sec):
        print(f"sound_freq: {freq=}, {sleep_sec=}")

    def sound_success(self):
        print("sound_success")
        self.sound_freq(1000, 0.05)
        self.sound_freq(2000, 0.05)

    def sound_error(self):
        print("sound_error")

    def turn(self, direction, angle=None, sleep_sec=None):
        print(f"turn: {direction=}, {angle=}")

    def drive(self, direction, cm=None, sleep_sec=None):
        print(f"drive: {direction=}")

    def stop(self):
        pass

    def stop_all(self):
        self.stop()
        self.clear_all_led()
        self.off_mini_led()

    def clear_all_led(self):
        pass

    def set_led(self, led_number, rgb):
        pass

    def set_all_led(self, rgb, brightness):
        pass

    def run_commands(self, command_list):
        self.status = STATUS_RUN_COMMANDS_STARTED
        for i, cmd in enumerate(command_list):
            print(cmd)
            action = cmd["action"]
            print(f"▶ Command {i + 1}: {action['type']}")

            # LEDをセットする
            if "led" in cmd:
                self.set_all_led(cmd["led"]["rgb"], 30)
            else:
                self.clear_all_led()

            #  車輪を動かす
            if action["type"] in ["forward", "reverse"]:
                if action.get("distance_cm"):
                    self.drive(action["type"], cm=action["distance_cm"])
                elif action.get("drive_sec"):
                    self.drive(action["type"], sleep_sec=action["drive_sec"])
                else:
                    raise ValueError("distance_cm or drive_sec must be provided")

            elif action["type"] == "turn":
                if action.get("angle"):
                    self.turn(action["direction"], angle=action["angle"])
                elif action.get("turn_sec"):
                    self.turn(action["direction"], sleep_sec=action["turn_sec"])
                else:
                    raise ValueError("angle or turn_sec must be provided")

            elif action["type"] == "stop":
                self.stop()

            else:
                print(f"⚠️ Unknown action: {action['type']} — skipping")
            self.stop()
            sleep(0.1)
        self.stop_all()
        print("✅ All commands executed")

    def on_mini_led(self):
        pass

    def off_mini_led(self):
        pass


class RealCar(Car):
    def __init__(self):
        super().__init__()
        self.buggy = KitronikPicoRobotBuggy()
        self.mini_led = Pin("LED", Pin.OUT)

    def sound_freq(self, freq, sleep_sec):
        super().sound_freq(freq, sleep_sec)
        self.buggy.soundFrequency(freq)
        sleep(sleep_sec)
        self.buggy.silence()

    def sound_error(self):
        super().sound_error()
        self.buggy.beepHorn()
        sleep(0.05)
        self.buggy.silence()
        self.buggy.beepHorn()
        sleep(0.05)
        self.buggy.silence()

    def turn(self, direction, angle=None, sleep_sec=None):
        super().turn(direction, angle, sleep_sec)
        if angle:
            sleep_sec = angle / self.degree_per_sec
        elif sleep_sec:
            sleep_sec = sleep_sec
        else:
            raise ValueError("angle or sleep_sec must be provided")

        if direction == "right":
            self.buggy.motorOn("l", "f", self.turn_speed)
            self.buggy.motorOn("r", "r", self.turn_speed)
        elif direction == "left":
            self.buggy.motorOn("l", "r", self.turn_speed)
            self.buggy.motorOn("r", "f", self.turn_speed)

        if sleep_sec <= 3:  # あまり長いと暴走するので、3秒までに制限する
            print("sleep...:", sleep_sec)
            sleep(sleep_sec)
        self.stop()

    def drive(self, direction, cm=None, sleep_sec=None):
        super().drive(direction, cm, sleep_sec)
        if cm:
            sleep_sec = cm / self.cm_per_sec
        elif sleep_sec:
            sleep_sec = sleep_sec
        else:
            raise ValueError("cm or sleep_sec must be provided")

        if direction == "forward":
            self.buggy.motorOn("l", "f", self.drive_speed)
            self.buggy.motorOn("r", "f", self.drive_speed)
        elif direction == "reverse":
            self.buggy.motorOn("l", "r", self.drive_speed)
            self.buggy.motorOn("r", "r", self.drive_speed)

        if sleep_sec < 5:  # あまり長いと暴走するので、5秒までに制限する
            print("sleep...:", sleep_sec)
            sleep(sleep_sec)
        self.stop()

    def stop(self):
        self.buggy.motorOff("r")
        self.buggy.motorOff("l")

    def clear_all_led(self):
        for i in range(4):
            self.buggy.clear(i)
        self.buggy.show()

    def set_led(self, led_number, rgb):
        self.buggy.setLED(led_number, rgb)
        self.buggy.show()

    def set_all_led(self, rgb, brightness):
        super().set_all_led(rgb, brightness)
        if rgb == (0, 0, 0):
            self.clear_all_led()
            return
        self.buggy.setBrightness(brightness)
        for i in range(4):
            self.buggy.setLED(i, rgb)
        self.buggy.show()

    def on_mini_led(self):
        self.mini_led.on()

    def off_mini_led(self):
        self.mini_led.off()


def check():
    sample_commands = [
        {
            "action": {
                "type": "forward",
                "distance_cm": 5,
            },
            "led": {"color": "off"},
        },
        {
            "action": {"type": "turn", "direction": "right", "angle": 90},
            "led": {"color": "off"},
        },
        {"action": {"type": "stop"}, "led": {"color": "off"}},
    ]

    try:
        car = RealCar()
        car.run_commands(sample_commands)
    except Exception as e:
        print("例外発生:", e)

    car.stop()
    print("end")
