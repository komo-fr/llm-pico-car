# Setup

This project is composed of two servers.

| Server | Runtime Environment | Role |
|--------|---------------------|------|
| **💻 Pico Controller Server** | PC (Python 3.13) | Receives user input via the Gradio UI and sends commands to the Pico Car Server |
| **🚜 Pico Car Server** | Raspberry Pi Pico WH (MicroPython)<br>Can also run on a PC using CPython in Mock mode | Receives commands and controls the car |

In Mock mode, both servers can run on a PC.

## 💻 Pico Controller Server Setup
1. On the PC where you will run the Pico Controller Server, run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install openai-whisper==20250625
```

2. Set the following environment variables:
```
# Obtain and set your OpenAI API key
OPENAI_API_KEY={Your OpenAI API key}

# API server URL for Mock mode (development/testing)
BASE_URL_MOCK=http://localhost:5001/

# API server URL for real hardware (Raspberry Pi Pico)
BASE_URL_REAL=http://192.168.11.49:5001/
```

3. (Optional) (Optional) If you want to enable logging with LangSmith, set the following environment variables:
```
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY={Your LangSmith API key}
LANGSMITH_PROJECT="pico-car"
```

## 🚜 Pico Car Server Setup
**When running in Mock mode on a CPython environment (e.g., a PC):**  
The Pico Car Server runs in the same virtual environment as the Pico Controller Server described above.

**When running on MicroPython on the Raspberry Pi Pico car kit:**
Follow these steps:

1. Follow the Kitronik tutorial to set up the kit and confirm that it works correctly.
    - [Online Tutorial - Autonomous Robotics Platform for Pico - Using the Mo – Kitronik Ltd](https://kitronik.co.uk/blogs/resources/online-tutorial-autonomous-robotics-platform-for-pico-motors)
2. Install Microdot on the Raspberry Pi Pico.
    - [Installation — Microdot documentation](https://microdot.readthedocs.io/en/latest/intro.html#micropython-installation)
    - Specifically, create a `microdot` directory on the Pico and manually copy the following files:
        - `__init__.py`
        - `microdot.py`
3. Copy the files under the `pico` directory in this repository to the Pico.

**The final directory structure on the Raspberry Pi Pico should look like this:**

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

4. Configure `SSID` and `PASSWORD` in `settings.py`. The IP address (`192.168.11.49`) should match the value specified in the `BASE_URL_REAL` environment variable mentioned above.

```
SSID = "..."  # Set your WiFi SSID
PASSWORD = "..."  # Set your WiFi password
IP_ADDRESS = "192.168.11.49"  # Match the BASE_URL_REAL environment variable
```
