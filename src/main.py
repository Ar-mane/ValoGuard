import sys
from pathlib import Path
import webview
from threading import Thread
from valoguard import ValoGuardBot

WINDOW_WIDTH = 450
WINDOW_HEIGHT = 360

_base = Path(sys._MEIPASS) if getattr(sys, 'frozen', False) else Path(__file__).parent.parent
_icon = str(_base / 'assets' / 'icon.ico')

bot = ValoGuardBot()


class Api:
    def start_bot(self):
        if not bot.running:
            thread = Thread(target=bot.run, daemon=True)
            thread.start()
            return True
        return False

    def stop_bot(self):
        bot.stop()
        return True

    def minimize_window(self):
        win.minimize()

    def close_window(self):
        bot.stop()
        win.destroy()


if __name__ == '__main__':
    api = Api()
    win = webview.create_window(
        'ValoGuard — Anti-AFK',
        str(_base / 'web' / 'index.html'),
        js_api=api,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=False,
        frameless=True,
    )
    bot.set_window(win)
    win.events.closed += lambda: (bot.stop(), sys.exit())
    webview.start(icon=_icon)

