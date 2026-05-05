# ValoGuard.py - Anti-AFK tool for VALORANT
# MIT License - Copyright (c) 2026 Qode
# See LICENSE file for full license text

import keyboard
import random
import time
import os
from datetime import datetime

LOG_DIR = "log"
LOG_FILE = os.path.join(LOG_DIR, "log.txt")
RUN_SECONDS = 4800  # 80 minutes
MOVE_HOLD_SECONDS = 2
MOVE_PAUSE_SECONDS = 1
LISTENER_LOOP_DELAY = 0.2

MOVE_ACTIONS = [
    ("FORWARD", "w"),
    ("BACKWARDS", "s"),
    ("LEFT", "a"),
    ("RIGHT", "d"),
    ("UP", "space"),
]

# VARS
_window = None
status = False


def current_time_str():
    return datetime.now().strftime("%H:%M:%S%p")


# CONTROL KEYBOARD
def perform_movement(key_to_press):
    keyboard.press(key_to_press)
    time.sleep(MOVE_HOLD_SECONDS)
    keyboard.release(key_to_press)
    time.sleep(MOVE_PAUSE_SECONDS)


def write_to_team(message):
    keyboard.press_and_release("enter")
    time.sleep(0.2)
    keyboard.write(message)
    keyboard.press_and_release("enter")


def write_to_global(message):
    keyboard.press_and_release("shift+enter")
    time.sleep(0.2)
    keyboard.write(message)
    keyboard.press_and_release("enter")


# RANDOM MOVEMENT
def move(index):
    try:
        action, key_to_press = MOVE_ACTIONS[index]
    except IndexError:
        return "ERROR: Index out of range"
    perform_movement(key_to_press)
    return action


def logger(timestamp, action, info):
    check_files()
    text = "[" + timestamp + "] action: " + action + " -> " + info
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(text + "\n")


def status_logger(text):
    check_files()
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(text + "\n")


def check_files():
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "a", encoding="utf-8"):
            pass


def set_window(window):
    global _window
    _window = window


def _notify_action():
    try:
        if _window:
            _window.evaluate_js('on_action()')
    except Exception:
        pass


def _notify_stop():
    try:
        if _window:
            _window.evaluate_js('stopBot()')
    except Exception:
        pass


def run():
    global status
    status = True
    start_time = time.monotonic()
    action_count = 0

    check_files()
    status_logger("[" + current_time_str() + "] ValoGuard started")

    while status is True:
        time.sleep(LISTENER_LOOP_DELAY)

        if (time.monotonic() - start_time) > RUN_SECONDS:
            status_logger("[" + current_time_str() + "] ValoGuard auto-stopped after 80 minutes")
            status = False
            _notify_stop()
            break

        index = random.randrange(len(MOVE_ACTIONS))
        action = move(index)
        logger(current_time_str(), action, str(action_count))
        action_count += 1
        _notify_action()

    status_logger("[" + current_time_str() + "] ValoGuard stopped")


def stop():
    global status
    status = False


# ── GUI adapter (used by main.py) ─────────────────────────────────────────────
# `ValoGuardBot` is a class that serves as an adapter for the GUI interface. It provides methods
# to set the window, start the ValoGuard anti-AFK tool, and stop the tool. The `run` method
# starts the ValoGuard tool, while the `stop` method stops it. The `running` attribute keeps
# track of whether the tool is currently running or not.
class ValoGuardBot:
    def __init__(self):
        self.running = False

    def set_window(self, window):
        set_window(window)

    def run(self):
        self.running = True
        run()
        self.running = False

    def stop(self):
        self.running = False
        stop()


if __name__ == "__main__":
    main()
