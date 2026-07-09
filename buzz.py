"""
Buzzer dashboard.

Reads button state from the ESP32-C5 over USB serial in a background thread,
and serves a fullscreen page that turns RED when the buzzer is pressed and
GREEN when it isn't.

Setup:  pip install flask pyserial
Run:    python buzz.py   ->   open http://localhost:5001

Important: close the Arduino IDE's Serial Monitor before running this.
Only one program can hold the serial port at a time.
"""

from flask import Flask, jsonify
import serial  # type: ignore[import]
from serial.tools import list_ports  # type: ignore[import]
import threading
import time

buzz = Flask(__name__)

BAUD = 115200
# Set this to your port to skip auto-detection, e.g. "/dev/tty.usbmodem1101"
# (mac), "/dev/ttyACM0" (Linux), or "COM5" (Windows). Leave None to auto-find.
FORCE_PORT = "/dev/cu.usbmodem101"

state = {"pressed": False, "connected": False}


def find_port():
    if FORCE_PORT:
        return FORCE_PORT
    for p in list_ports.comports():
        name = p.device.lower()
        if any(k in name for k in
               ("usbmodem", "usbserial", "ttyusb", "ttyacm", "wchusb", "slab")):
            return p.device
    return None


def read_serial():
    while True:
        port = find_port()
        if not port:
            state["connected"] = False
            time.sleep(1)
            continue
        try:
            ser = serial.Serial(port, BAUD, timeout=1)
            state["connected"] = True
            print(f"[serial] connected to {port}")
            while True:
                line = ser.readline().decode(errors="ignore").strip()
                if line == "1":
                    state["pressed"] = True
                elif line == "0":
                    state["pressed"] = False
        except serial.SerialException as e:
            print(f"[serial] disconnected ({e}); retrying...")
            state["connected"] = False
            state["pressed"] = False
            time.sleep(1)


threading.Thread(target=read_serial, daemon=True).start()


@buzz.route("/state")
def get_state():
    return jsonify(state)


HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Buzzer Dashboard</title>
<style>
  html, body { margin: 0; height: 100%; }
  #screen {
    height: 100vh;
    display: flex; align-items: center; justify-content: center;
    font-family: system-ui, -apple-system, sans-serif;
    color: white; font-size: 5rem; font-weight: 800; letter-spacing: 0.05em;
    background: #16a34a;
    transition: background 60ms linear;
  }
  #status {
    position: fixed; bottom: 1.25rem; left: 50%; transform: translateX(-50%);
    font-family: system-ui, sans-serif; font-size: 0.95rem;
    color: white; opacity: 0.85;
  }
</style>
</head>
<body>
  <div id="screen">READY</div>
  <div id="status">connecting...</div>
  <script>
    async function poll() {
      try {
        const r = await fetch('/state');
        const s = await r.json();
        const screen = document.getElementById('screen');
        if (s.pressed) {
          screen.style.background = '#dc2626';
          screen.textContent = 'BUZZ!';
        } else {
          screen.style.background = '#16a34a';
          screen.textContent = 'READY';
        }
        document.getElementById('status').textContent =
          s.connected ? '\u25CF ESP32 connected' : '\u25CB waiting for ESP32...';
      } catch (e) {
        document.getElementById('status').textContent = 'server error';
      }
    }
    setInterval(poll, 100);
    poll();
  </script>
</body>
</html>"""


@buzz.route("/")
def index():
    return HTML


if __name__ == "__main__":
    buzz.run(host="0.0.0.0", port=5001, threaded=True)