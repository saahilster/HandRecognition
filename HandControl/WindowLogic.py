# WindowLogic.py (or wherever your utils live)
import sys, time
import pyautogui as pg

pg.FAILSAFE = True
pg.PAUSE = 0.05

cooldown = 1
_last = 0.0

def throttle():
    global _last
    now = time.time()
    if now - _last < cooldown:
        return False
    _last = now
    return True

def minimize():
    if not throttle(): 
        return
    if sys.platform.startswith("win"):
        pg.hotkey("win", "down")
        time.sleep(0.015)
        pg.hotkey("win", "down")

def maximize():
    if not throttle(): 
        return
    if sys.platform.startswith("win"):
        pg.hotkey("alt", "tab")

def StopProgram():
    if not sys.platform.startswith("win"):
        return
    pg.keyDown("q")

class Scroller:
    def __init__(self, interval=0.20, key="down", platform_guard=True):
        self.interval = interval
        self.key = key
        self.platform_guard = platform_guard
        self.active = False
        self._next_at = 0.0

    def start(self):
        if not self.active:
            self.active = True
            self._next_at = time.monotonic()  # fire on next update()

    def stop(self):
        self.active = False

    def update(self):
        if not self.active:
            return
        if self.platform_guard and not sys.platform.startswith("win"):
            return
        now = time.monotonic()
        if now >= self._next_at:
            try:
                pg.press(self.key)   # correct for single key
            except Exception as e:
                print(f"[Scroller] press error: {e!r}")
            finally:
                self._next_at = now + self.interval
