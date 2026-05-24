"""
i_am_bad_at_games v1.0
Recoil & Rapid Fire macro assistant
Run: pip install customtkinter pynput pillow
     python macro_assistant.py
"""

import customtkinter as ctk
from tkinter import StringVar, messagebox, simpledialog
import threading
import time
import json
import os
import random
import ctypes
from pynput import mouse, keyboard
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button
from PIL import Image
import sys
import traceback
import subprocess

# -------------------------------
# App Data Paths & Logging
# -------------------------------
APP_NAME = "i_am_bad_at_games v1.0"
DATA_DIR = os.path.join(os.environ['USERPROFILE'], '.macro_assistant')
CONFIG_FILE = os.path.join(DATA_DIR, 'presets.json')
APP_SETTINGS_FILE = os.path.join(DATA_DIR, 'app_settings.json')
LOG_FILE = os.path.join(DATA_DIR, 'macro_log.txt')

os.makedirs(DATA_DIR, exist_ok=True)

def log(msg, error=False):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - {msg}\n")
        if error:
            traceback.print_exc(file=f)
    print(f"{'ERROR' if error else 'INFO'}: {msg}")

# -------------------------------
# Mouse Movement (Windows)
# -------------------------------
def move_mouse(dx, dy):
    ctypes.windll.user32.mouse_event(0x0001, int(dx), int(dy), 0, 0)

def click_mouse():
    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
    time.sleep(0.01)
    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)

# -------------------------------
# Global Button State Tracker
# -------------------------------
class ButtonState:
    def __init__(self):
        self.left = False
        self.right = False
        self.middle = False
        self.x1 = False
        self.x2 = False

    def update(self, button, pressed):
        if button == Button.left:
            self.left = pressed
        elif button == Button.right:
            self.right = pressed
        elif button == Button.middle:
            self.middle = pressed
        elif button == Button.x1:
            self.x1 = pressed
        elif button == Button.x2:
            self.x2 = pressed

button_state = ButtonState()

# -------------------------------
# Recoil Macro (F1 toggles)
# -------------------------------
recoil_settings = {
    "vertical": 5.0,
    "horizontal": 0.0,
    "sensitivity": 1.0,
    "sleep_ms": 7,
    "first_shot_delay": 0,
    "mode": "LMB",
    "legit_mode": False,
    "random_amount": 2
}
recoil_enabled = False
recoil_active = False
recoil_thread = None
recoil_running = True

def recoil_loop():
    global recoil_active, recoil_running
    first_shot = True
    while recoil_running:
        try:
            if recoil_enabled:
                if recoil_settings["mode"] == "LMB":
                    active = button_state.left
                else:
                    active = button_state.left and button_state.right
                if active != recoil_active:
                    recoil_active = active
                    if not recoil_active:
                        first_shot = True
                if recoil_active:
                    if first_shot and recoil_settings["first_shot_delay"] > 0:
                        time.sleep(recoil_settings["first_shot_delay"] / 1000.0)
                        first_shot = False
                    v = recoil_settings["vertical"] * recoil_settings["sensitivity"]
                    h = recoil_settings["horizontal"] * recoil_settings["sensitivity"]
                    if recoil_settings["legit_mode"]:
                        v += random.uniform(-recoil_settings["random_amount"], recoil_settings["random_amount"])
                        h += random.uniform(-recoil_settings["random_amount"], recoil_settings["random_amount"])
                    move_mouse(round(h), round(v))
                    time.sleep(recoil_settings["sleep_ms"] / 1000.0)
                else:
                    time.sleep(0.005)
            else:
                time.sleep(0.01)
        except Exception as e:
            log(f"Recoil loop error: {e}", error=True)
            time.sleep(0.1)

def start_recoil_thread():
    global recoil_thread, recoil_running
    recoil_running = True
    if recoil_thread is None or not recoil_thread.is_alive():
        recoil_thread = threading.Thread(target=recoil_loop, daemon=True)
        recoil_thread.start()
        log("Recoil thread started")

def toggle_recoil():
    global recoil_enabled
    recoil_enabled = not recoil_enabled
    log(f"Recoil macro toggled {'ON' if recoil_enabled else 'OFF'}")
    try:
        app.update_recoil_status()
        app.horse_speak(f"Recoil macro {'ON' if recoil_enabled else 'OFF'}")
    except:
        pass
    return recoil_enabled

# -------------------------------
# Rapid Fire (F3 toggles)
# -------------------------------
rapid_settings = {
    "activation_type": "key",
    "key": "z",
    "mouse_button": "left",
    "interval": 0.05
}
rapid_enabled = False
rapid_active = False
rapid_thread = None
rapid_running = True

def rapid_loop():
    global rapid_active, rapid_running
    while rapid_running:
        try:
            if rapid_enabled:
                if rapid_settings["activation_type"] == "key":
                    active = rapid_active
                else:
                    btn = rapid_settings["mouse_button"]
                    if btn == "left":
                        active = button_state.left
                    elif btn == "right":
                        active = button_state.right
                    elif btn == "middle":
                        active = button_state.middle
                    elif btn == "x1":
                        active = button_state.x1
                    elif btn == "x2":
                        active = button_state.x2
                    else:
                        active = False
                if active:
                    click_mouse()
                    time.sleep(rapid_settings["interval"])
                else:
                    time.sleep(0.005)
            else:
                time.sleep(0.01)
        except Exception as e:
            log(f"Rapid loop error: {e}", error=True)
            time.sleep(0.1)

def start_rapid_thread():
    global rapid_thread, rapid_running
    rapid_running = True
    if rapid_thread is None or not rapid_thread.is_alive():
        rapid_thread = threading.Thread(target=rapid_loop, daemon=True)
        rapid_thread.start()
        log("Rapid fire thread started")

def toggle_rapid():
    global rapid_enabled
    rapid_enabled = not rapid_enabled
    log(f"Rapid fire toggled {'ON' if rapid_enabled else 'OFF'}")
    try:
        app.update_rapid_status()
        app.horse_speak(f"Rapid fire {'ON' if rapid_enabled else 'OFF'}")
    except:
        pass
    return rapid_enabled

def on_rapid_key_press(key):
    global rapid_active
    if not rapid_enabled or rapid_settings["activation_type"] != "key":
        return
    try:
        if hasattr(key, 'char') and key.char is not None:
            if key.char == rapid_settings["key"]:
                rapid_active = True
        else:
            key_str = str(key).replace("Key.", "")
            if key_str == rapid_settings["key"]:
                rapid_active = True
    except:
        pass

def on_rapid_key_release(key):
    global rapid_active
    if not rapid_enabled or rapid_settings["activation_type"] != "key":
        return
    try:
        if hasattr(key, 'char') and key.char is not None:
            if key.char == rapid_settings["key"]:
                rapid_active = False
        else:
            key_str = str(key).replace("Key.", "")
            if key_str == rapid_settings["key"]:
                rapid_active = False
    except:
        pass

# -------------------------------
# Quick‑save with F10
# -------------------------------
def on_f10_press(key):
    if key == Key.f10:
        if 'app' in globals():
            app.after(0, lambda: app.quick_save_dialog())
        return True

# -------------------------------
# Global Hotkeys (F1, F3, Insert)
# -------------------------------
def global_hotkey_handler(key):
    try:
        if key == Key.f1:
            toggle_recoil()
        elif key == Key.f3:
            toggle_rapid()
        elif key == Key.insert:
            app.toggle_stealth()
    except:
        pass

# -------------------------------
# Custom UI Components
# -------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG_DARK    = "#0d1117"
BG_PANEL   = "#161b22"
BG_CARD    = "#1c2230"
BG_SIDEBAR = "#0d1117"
ACCENT     = "#00c2ff"
ACCENT2    = "#0077ff"
TEXT_MAIN  = "#e6edf3"
TEXT_SUB   = "#8b949e"
BORDER     = "#30363d"
GREEN      = "#3fb950"
KEY_BG     = "#21262d"
KEY_FG     = "#8b949e"

class KeyBadge(ctk.CTkLabel):
    def __init__(self, parent, key_text, **kwargs):
        super().__init__(parent, text=key_text, width=36, height=22,
                         fg_color=KEY_BG, text_color=KEY_FG, corner_radius=4,
                         font=ctk.CTkFont("Consolas", 11, "bold"), **kwargs)

class SliderRow(ctk.CTkFrame):
    def __init__(self, parent, label, from_=0, to=100, default=50, resolution=1, unit="", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.resolution = resolution
        self.unit = unit
        ctk.CTkLabel(self, text=label, text_color=TEXT_MAIN,
                     font=ctk.CTkFont("Segoe UI", 12)).pack(anchor="w")
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=(4, 0))
        self.val_var = StringVar()
        steps = int((to - from_) / resolution) if resolution > 0 else 100
        self.slider = ctk.CTkSlider(row, from_=from_, to=to, number_of_steps=steps,
                                    progress_color=ACCENT2, button_color=ACCENT,
                                    fg_color=BORDER, width=200,
                                    command=self._on_change)
        self.slider.set(default)
        self.slider.pack(side="left")
        self.val_label = ctk.CTkLabel(row, textvariable=self.val_var, text_color=ACCENT,
                                      font=ctk.CTkFont("Consolas", 11, "bold"), width=46)
        self.val_label.pack(side="left", padx=(8, 0))
        self._on_change(default)

    def _on_change(self, v):
        if self.resolution < 1:
            self.val_var.set(f"{float(v):.1f}{self.unit}")
        else:
            self.val_var.set(f"{int(v)}{self.unit}")

    def get(self):
        return self.slider.get()

    def set(self, v):
        self.slider.set(v)
        self._on_change(v)

class ToggleRow(ctk.CTkFrame):
    def __init__(self, parent, label, default=True, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        ctk.CTkLabel(self, text=label, text_color=TEXT_MAIN,
                     font=ctk.CTkFont("Segoe UI", 12)).pack(side="left")
        self.switch = ctk.CTkSwitch(self, text="", width=44, height=22,
                                    progress_color=ACCENT2, button_color=ACCENT,
                                    fg_color=BORDER)
        self.switch.pack(side="left", padx=(12, 0))
        self.switch.select() if default else self.switch.deselect()

    def get(self):
        return self.switch.get()

    def set(self, v):
        self.switch.select() if v else self.switch.deselect()

class SectionCard(ctk.CTkFrame):
    def __init__(self, parent, title, icon="", **kwargs):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=10,
                         border_width=1, border_color=BORDER, **kwargs)
        self.expanded = True
        header = ctk.CTkFrame(self, fg_color="transparent", cursor="hand2")
        header.pack(fill="x", padx=14, pady=(10, 8))
        ctk.CTkLabel(header, text=f"{icon}  {title}", text_color=TEXT_SUB,
                     font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(side="left")
        self.arrow = ctk.CTkLabel(header, text="▾", text_color=TEXT_SUB,
                                  font=ctk.CTkFont("Segoe UI", 12))
        self.arrow.pack(side="right")
        for w in [header] + header.winfo_children():
            w.bind("<Button-1>", self._toggle)
        self.sep = ctk.CTkFrame(self, fg_color=BORDER, height=1)
        self.sep.pack(fill="x", padx=14)
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="x", padx=14, pady=10)

    def _toggle(self, _=None):
        self.expanded = not self.expanded
        if self.expanded:
            self.sep.pack(fill="x", padx=14)
            self.body.pack(fill="x", padx=14, pady=10)
            self.arrow.configure(text="▾")
        else:
            self.sep.pack_forget()
            self.body.pack_forget()
            self.arrow.configure(text="▸")

class SidebarBtn(ctk.CTkButton):
    def __init__(self, parent, icon, label, active=False, **kwargs):
        super().__init__(parent, text=f"{icon}\n{label}", width=60, height=60,
                         fg_color="#2a3042" if active else "transparent",
                         hover_color="#1c2230",
                         text_color=TEXT_MAIN if active else TEXT_SUB,
                         font=ctk.CTkFont("Segoe UI", 9),
                         corner_radius=8, **kwargs)

# -------------------------------
# Pages
# -------------------------------
class RecoilPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BG_DARK, corner_radius=0, **kwargs)
        self.columnconfigure((0, 1), weight=1)
        self.widgets = {}

        # Vertical
        card = SectionCard(self, "VERTICAL RECOIL", "↓")
        card.grid(row=0, column=0, padx=(12, 6), pady=8, sticky="nsew")
        self.widgets["vertical"] = SliderRow(card.body, "Vertical (-10 to +10)", -10, 10, 5.0, 0.1, "")
        self.widgets["vertical"].pack(fill="x", pady=(0, 10))
        self.widgets["horizontal"] = SliderRow(card.body, "Horizontal (-2.5 to +2.5)", -2.5, 2.5, 0.0, 0.1, "")
        self.widgets["horizontal"].pack(fill="x", pady=(0, 10))
        self.widgets["sensitivity"] = SliderRow(card.body, "Sensitivity (x)", 0.1, 2.0, 1.0, 0.1, "")
        self.widgets["sensitivity"].pack(fill="x", pady=(0, 10))
        self.widgets["sleep"] = SliderRow(card.body, "Sleep Time (ms)", 1, 50, 7, 1, "")
        self.widgets["sleep"].pack(fill="x", pady=(0, 10))
        self.widgets["first_shot"] = SliderRow(card.body, "First Shot Delay (ms)", 0, 500, 0, 1, "")
        self.widgets["first_shot"].pack(fill="x", pady=(0, 10))

        # Mode
        mode_frame = ctk.CTkFrame(card.body, fg_color="transparent")
        mode_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(mode_frame, text="Activation Mode", text_color=TEXT_MAIN,
                     font=ctk.CTkFont("Segoe UI", 12)).pack(side="left")
        self.widgets["mode"] = StringVar(value="LMB")
        mode_menu = ctk.CTkOptionMenu(mode_frame, variable=self.widgets["mode"],
                                      values=["LMB", "RMB+LMB"],
                                      width=100, fg_color=KEY_BG,
                                      button_color=ACCENT2,
                                      dropdown_fg_color=BG_CARD,
                                      text_color=TEXT_MAIN,
                                      command=self._update_mode)
        mode_menu.pack(side="right", padx=5)

        # Legit mode
        self.widgets["legit_mode"] = ctk.BooleanVar(value=False)
        legit_switch = ctk.CTkSwitch(card.body, text="✨ Legit Mode (randomness)",
                                     variable=self.widgets["legit_mode"],
                                     command=self._update_legit,
                                     progress_color=ACCENT2, button_color=ACCENT,
                                     fg_color=BORDER)
        legit_switch.pack(anchor="w", pady=5)

        # Random amount
        self.widgets["random_amount"] = SliderRow(card.body, "Randomization (pixels)", 0, 10, 2, 1, "")
        self.widgets["random_amount"].pack(fill="x", pady=5)

        # Status
        self.status_label = ctk.CTkLabel(card.body, text="● DISARMED", text_color="#ff5555",
                                         font=ctk.CTkFont("Segoe UI", 12, "bold"))
        self.status_label.pack(pady=10)
        ctk.CTkLabel(card.body, text="F1 toggles ON/OFF", text_color=TEXT_SUB,
                     font=ctk.CTkFont("Segoe UI", 9)).pack()

    def _update_mode(self, value):
        global recoil_settings
        recoil_settings["mode"] = value
        self.widgets["mode"].set(value)

    def _update_legit(self):
        global recoil_settings
        recoil_settings["legit_mode"] = self.widgets["legit_mode"].get()

    def get_config(self):
        return {
            "vertical": self.widgets["vertical"].get(),
            "horizontal": self.widgets["horizontal"].get(),
            "sensitivity": self.widgets["sensitivity"].get(),
            "sleep_ms": int(self.widgets["sleep"].get()),
            "first_shot_delay": int(self.widgets["first_shot"].get()),
            "mode": self.widgets["mode"].get(),
            "legit_mode": self.widgets["legit_mode"].get(),
            "random_amount": int(self.widgets["random_amount"].get())
        }

    def load_config(self, data):
        global recoil_settings   # Moved to top of function
        for k, v in data.items():
            if k in self.widgets and hasattr(self.widgets[k], "set"):
                self.widgets[k].set(v)
            elif k == "mode" and k in self.widgets:
                self.widgets["mode"].set(v)
                recoil_settings["mode"] = v
            elif k == "legit_mode" and k in self.widgets:
                self.widgets["legit_mode"].set(v)
                recoil_settings["legit_mode"] = v

    def update_status(self, enabled):
        self.status_label.configure(text="● ARMED" if enabled else "● DISARMED",
                                    text_color=GREEN if enabled else "#ff5555")

class RapidFirePage(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BG_DARK, corner_radius=0, **kwargs)
        self.columnconfigure((0, 1), weight=1)
        self.widgets = {}

        card = SectionCard(self, "RAPID FIRE", "⚡")
        card.grid(row=0, column=0, padx=(12, 6), pady=8, sticky="nsew")

        # Activation type
        type_frame = ctk.CTkFrame(card.body, fg_color="transparent")
        type_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(type_frame, text="Activation Type", text_color=TEXT_MAIN,
                     font=ctk.CTkFont("Segoe UI", 12)).pack(side="left")
        self.widgets["activation_type"] = StringVar(value="key")
        type_menu = ctk.CTkOptionMenu(type_frame, variable=self.widgets["activation_type"],
                                      values=["key", "mouse"],
                                      width=100, fg_color=KEY_BG,
                                      button_color=ACCENT2,
                                      dropdown_fg_color=BG_CARD,
                                      text_color=TEXT_MAIN,
                                      command=self._update_activation_type)
        type_menu.pack(side="right", padx=5)

        # Key selection
        self.key_frame = ctk.CTkFrame(card.body, fg_color="transparent")
        self.key_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(self.key_frame, text="Keyboard Key:", text_color=TEXT_SUB).pack(side="left", padx=5)
        self.widgets["key_label"] = ctk.CTkLabel(self.key_frame, text="z",
                                                width=50, height=28, fg_color=KEY_BG,
                                                text_color=ACCENT, corner_radius=4,
                                                font=ctk.CTkFont("Consolas", 11, "bold"))
        self.widgets["key_label"].pack(side="left", padx=10)
        ctk.CTkButton(self.key_frame, text="Select Key", width=80, height=28,
                      fg_color=KEY_BG, hover_color=BORDER,
                      text_color=TEXT_MAIN, command=self.select_key).pack(side="left")
        self.widgets["key"] = "z"

        # Mouse button
        self.mouse_frame = ctk.CTkFrame(card.body, fg_color="transparent")
        self.mouse_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(self.mouse_frame, text="Mouse Button:", text_color=TEXT_SUB).pack(side="left", padx=5)
        self.widgets["mouse_button"] = StringVar(value="left")
        mouse_menu = ctk.CTkOptionMenu(self.mouse_frame, variable=self.widgets["mouse_button"],
                                       values=["left", "right", "middle", "x1", "x2"],
                                       width=100, fg_color=KEY_BG,
                                       button_color=ACCENT2,
                                       dropdown_fg_color=BG_CARD,
                                       text_color=TEXT_MAIN,
                                       command=self._update_mouse_button)
        mouse_menu.pack(side="left", padx=10)

        # Interval
        self.widgets["interval"] = SliderRow(card.body, "Click Interval (s)", 0.01, 0.5, 0.05, 0.01, "")
        self.widgets["interval"].pack(fill="x", pady=5)

        # Status
        self.status_label = ctk.CTkLabel(card.body, text="● DISARMED", text_color="#ff5555",
                                         font=ctk.CTkFont("Segoe UI", 12, "bold"))
        self.status_label.pack(pady=10)
        ctk.CTkLabel(card.body, text="F3 toggles ON/OFF", text_color=TEXT_SUB,
                     font=ctk.CTkFont("Segoe UI", 9)).pack()

        self._on_activation_change()

    def _update_activation_type(self, value):
        global rapid_settings
        rapid_settings["activation_type"] = value
        self.widgets["activation_type"].set(value)
        self._on_activation_change()

    def _update_mouse_button(self, value):
        global rapid_settings
        rapid_settings["mouse_button"] = value
        self.widgets["mouse_button"].set(value)

    def _on_activation_change(self, _=None):
        if self.widgets["activation_type"].get() == "key":
            self.key_frame.pack(fill="x", pady=5)
            self.mouse_frame.pack_forget()
        else:
            self.mouse_frame.pack(fill="x", pady=5)
            self.key_frame.pack_forget()

    def select_key(self):
        """Non‑blocking key selection using a separate thread."""
        self.horse_speak("Press any key to set...")
        def listen():
            def on_press(key):
                try:
                    if hasattr(key, 'char') and key.char is not None:
                        new_key = key.char
                    else:
                        new_key = str(key).replace("Key.", "")
                except:
                    new_key = str(key)
                app.after(0, lambda: self._set_key(new_key))
                return False
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        threading.Thread(target=listen, daemon=True).start()

    def _set_key(self, new_key):
        global rapid_settings
        rapid_settings["key"] = new_key
        self.widgets["key"] = new_key
        self.widgets["key_label"].configure(text=new_key)
        self.horse_speak(f"Rapid key set to {new_key}")

    def horse_speak(self, msg):
        if hasattr(app, "horse_speak"):
            app.horse_speak(msg)

    def get_config(self):
        return {
            "activation_type": self.widgets["activation_type"].get(),
            "key": self.widgets["key"],
            "mouse_button": self.widgets["mouse_button"].get(),
            "interval": self.widgets["interval"].get()
        }

    def load_config(self, data):
        global rapid_settings   # Moved to top
        for k, v in data.items():
            if k in self.widgets and hasattr(self.widgets[k], "set"):
                self.widgets[k].set(v)
            elif k == "key":
                self._set_key(v)
            elif k == "activation_type":
                self._update_activation_type(v)
            elif k == "mouse_button":
                self._update_mouse_button(v)

    def update_status(self, enabled):
        self.status_label.configure(text="● ARMED" if enabled else "● DISARMED",
                                    text_color=GREEN if enabled else "#ff5555")

class SettingsPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, get_all_config, load_all_config, **kwargs):
        super().__init__(parent, fg_color=BG_DARK, corner_radius=0, **kwargs)
        self._get_all = get_all_config
        self._load_all = load_all_config

        card = SectionCard(self, "PRESETS", "💾")
        card.pack(fill="x", padx=12, pady=8)

        self.status = ctk.CTkLabel(card.body, text="", text_color=ACCENT,
                                   font=ctk.CTkFont("Segoe UI", 11))
        self.status.pack(anchor="w", pady=(0, 8))

        # Preset name
        row1 = ctk.CTkFrame(card.body, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        ctk.CTkLabel(row1, text="Preset Name:", text_color=TEXT_MAIN).pack(side="left", padx=5)
        self.preset_entry = ctk.CTkEntry(row1, width=160, fg_color=KEY_BG, text_color=TEXT_MAIN)
        self.preset_entry.pack(side="left", padx=10)
        ctk.CTkButton(row1, text="💾 Save", width=70, command=self.save_preset,
                      fg_color=KEY_BG, hover_color=BORDER, text_color=TEXT_MAIN).pack(side="left", padx=5)
        ctk.CTkButton(row1, text="📂 Load", width=70, command=self.load_preset,
                      fg_color=KEY_BG, hover_color=BORDER, text_color=TEXT_MAIN).pack(side="left", padx=5)
        ctk.CTkButton(row1, text="🗑️ Delete", width=70, command=self.delete_preset,
                      fg_color=KEY_BG, hover_color=BORDER, text_color=TEXT_MAIN).pack(side="left", padx=5)

        row2 = ctk.CTkFrame(card.body, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        ctk.CTkLabel(row2, text="Load from list:", text_color=TEXT_MAIN).pack(side="left", padx=5)
        self.preset_combo = ctk.CTkOptionMenu(row2, variable=StringVar(), values=[],
                                              width=200, fg_color=KEY_BG,
                                              button_color=ACCENT2,
                                              dropdown_fg_color=BG_CARD,
                                              text_color=TEXT_MAIN)
        self.preset_combo.pack(side="left", padx=10)
        ctk.CTkButton(row2, text="⟳ Refresh", width=80, command=self.refresh_preset_list,
                      fg_color=KEY_BG, hover_color=BORDER, text_color=TEXT_MAIN).pack(side="left", padx=5)

        ctk.CTkButton(card.body, text="📂 Open Presets Folder", command=self.open_presets_folder,
                      fg_color=KEY_BG, hover_color=BORDER, text_color=TEXT_MAIN,
                      font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(pady=10)

        path_label = ctk.CTkLabel(card.body, text=f"📍 Presets saved to:\n{CONFIG_FILE}",
                                  text_color=TEXT_SUB, font=ctk.CTkFont("Segoe UI", 8))
        path_label.pack(pady=5)

        self.refresh_preset_list()

    def save_preset(self):
        name = self.preset_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter a preset name")
            return
        presets = self.load_presets()
        presets[name] = self._get_all()
        with open(CONFIG_FILE, 'w') as f:
            json.dump(presets, f, indent=2)
        self.refresh_preset_list()
        self.preset_combo.set(name)
        self.status.configure(text=f"✔ Saved '{name}'")

    def load_preset(self):
        name = self.preset_combo.get()
        if not name:
            return
        presets = self.load_presets()
        if name in presets:
            self._load_all(presets[name])
            self.status.configure(text=f"✔ Loaded '{name}'")
        else:
            messagebox.showerror("Error", f"Preset '{name}' not found")

    def delete_preset(self):
        name = self.preset_combo.get()
        if not name:
            return
        presets = self.load_presets()
        if name in presets:
            del presets[name]
            with open(CONFIG_FILE, 'w') as f:
                json.dump(presets, f, indent=2)
            self.refresh_preset_list()
            self.status.configure(text=f"Deleted '{name}'")

    def load_presets(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}

    def refresh_preset_list(self):
        presets = self.load_presets()
        names = list(presets.keys())
        self.preset_combo.configure(values=names)
        if names:
            self.preset_combo.set(names[0])
        else:
            self.preset_combo.set("")

    def open_presets_folder(self):
        if os.path.exists(DATA_DIR):
            subprocess.Popen(f'explorer "{DATA_DIR}"')
        else:
            messagebox.showerror("Error", f"Folder not found: {DATA_DIR}")

# -------------------------------
# Main App
# -------------------------------
class MacroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("860x640")
        self.minsize(820, 580)
        self.configure(fg_color=BG_DARK)
        self.attributes("-topmost", True)
        self.stealth = False
        self.tray_icon = None
        self._active_page = None
        self._sidebar_btns = []

        self._build_layout()
        self.load_last_preset()
        self.start_listeners()
        self.setup_tray()

        start_recoil_thread()
        start_rapid_thread()
        self.horse_speak("Ready - F1 recoil, F3 rapid, F10 save")

    def _build_layout(self):
        # Sidebar
        sidebar = ctk.CTkFrame(self, width=72, fg_color=BG_SIDEBAR,
                               corner_radius=0, border_width=1, border_color=BORDER)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        ctk.CTkLabel(sidebar, text="⧉", text_color=ACCENT,
                     font=ctk.CTkFont("Segoe UI", 22, "bold")).pack(pady=(16, 20))

        nav = [("🎯", "Recoil"), ("⚡", "Rapid\nFire"), ("⚙", "Settings")]
        for i, (icon, lbl) in enumerate(nav):
            btn = SidebarBtn(sidebar, icon, lbl, active=(i == 0))
            btn.configure(command=lambda idx=i: self._switch_page(idx))
            btn.pack(pady=4, padx=6)
            self._sidebar_btns.append(btn)

        # Main area
        main = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        main.pack(side="left", fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(main, fg_color=BG_PANEL, height=76,
                              corner_radius=0, border_width=1, border_color=BORDER)
        header.pack(fill="x")
        header.pack_propagate(False)

        thumb = ctk.CTkFrame(header, width=90, height=52,
                             fg_color="#1a1a2e", corner_radius=6)
        thumb.pack(side="left", padx=(14, 10), pady=12)
        thumb.pack_propagate(False)
        ctk.CTkLabel(thumb, text="🎮", font=ctk.CTkFont("Segoe UI", 22)).place(relx=0.5, rely=0.5, anchor="center")

        info = ctk.CTkFrame(header, fg_color="transparent")
        info.pack(side="left", fill="y", pady=12)
        ctk.CTkLabel(info, text=APP_NAME, text_color=TEXT_MAIN,
                     font=ctk.CTkFont("Segoe UI", 15, "bold")).pack(anchor="w")
        ctk.CTkLabel(info, text="Recoil & Rapid Fire Macro", text_color=TEXT_SUB,
                     font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w", pady=(2, 0))

        self.page_label = ctk.CTkLabel(header, text="Recoil", text_color=ACCENT,
                                       font=ctk.CTkFont("Segoe UI", 13, "bold"))
        self.page_label.pack(side="right", padx=20)

        # Content area
        self.content = ctk.CTkFrame(main, fg_color=BG_DARK, corner_radius=0)
        self.content.pack(fill="both", expand=True)

        # Pages
        self.recoil_page = RecoilPage(self.content)
        self.rapid_page = RapidFirePage(self.content)
        self.settings_page = SettingsPage(self.content,
                                          get_all_config=self.get_all_config,
                                          load_all_config=self.load_all_config)

        self.pages = [self.recoil_page, self.rapid_page, self.settings_page]
        self.page_names = ["Recoil", "Rapid Fire", "Settings"]

        self._switch_page(0)

        # Status bar
        self.status_label = ctk.CTkLabel(main, text="💬 Ready", fg_color=BG_PANEL,
                                         text_color=TEXT_SUB, anchor="w",
                                         font=ctk.CTkFont("Segoe UI", 9))
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=(0, 5))

    def _switch_page(self, idx):
        for p in self.pages:
            p.pack_forget()
        self.pages[idx].pack(fill="both", expand=True)
        self.page_label.configure(text=self.page_names[idx])
        for i, btn in enumerate(self._sidebar_btns):
            btn.configure(fg_color="#2a3042" if i == idx else "transparent",
                          text_color=TEXT_MAIN if i == idx else TEXT_SUB)
        self._active_page = idx

    def get_all_config(self):
        return {
            "recoil": self.recoil_page.get_config(),
            "rapid": self.rapid_page.get_config()
        }

    def load_all_config(self, data):
        if "recoil" in data:
            self.recoil_page.load_config(data["recoil"])
            # Also update global settings
            global recoil_settings
            for k, v in data["recoil"].items():
                if k in recoil_settings:
                    recoil_settings[k] = v
        if "rapid" in data:
            self.rapid_page.load_config(data["rapid"])
            global rapid_settings
            for k, v in data["rapid"].items():
                if k in rapid_settings:
                    rapid_settings[k] = v

    def load_last_preset(self):
        if os.path.exists(APP_SETTINGS_FILE):
            try:
                with open(APP_SETTINGS_FILE, 'r') as f:
                    app_data = json.load(f)
                    if "last_preset" in app_data:
                        last = app_data["last_preset"]
                        presets = self.settings_page.load_presets()
                        if last in presets:
                            self.load_all_config(presets[last])
                            self.horse_speak(f"Loaded last preset: {last}")
                            return
            except:
                pass
        self.horse_speak("Using default settings")

    def save_app_settings(self):
        app_data = {"last_preset": self.settings_page.preset_combo.get()}
        with open(APP_SETTINGS_FILE, 'w') as f:
            json.dump(app_data, f)

    def horse_speak(self, msg):
        self.status_label.configure(text=f"💬 {msg}")
        log(msg)

    def update_recoil_status(self):
        self.recoil_page.update_status(recoil_enabled)

    def update_rapid_status(self):
        self.rapid_page.update_status(rapid_enabled)

    def quick_save_dialog(self):
        name = simpledialog.askstring("Quick Save", "Enter preset name:", parent=self)
        if name:
            presets = self.settings_page.load_presets()
            presets[name] = self.get_all_config()
            with open(CONFIG_FILE, 'w') as f:
                json.dump(presets, f, indent=2)
            self.settings_page.refresh_preset_list()
            self.settings_page.preset_combo.set(name)
            self.horse_speak(f"Quick-saved preset '{name}'")

    # ----- Listeners & Tray -----
    def start_listeners(self):
        self.mouse_state_listener = mouse.Listener(on_click=self.on_global_mouse_click)
        self.mouse_state_listener.start()
        self.global_kb = keyboard.Listener(on_press=global_hotkey_handler)
        self.global_kb.start()
        self.rapid_kb = keyboard.Listener(on_press=on_rapid_key_press, on_release=on_rapid_key_release)
        self.rapid_kb.start()
        self.f10_listener = keyboard.Listener(on_press=on_f10_press)
        self.f10_listener.start()

    def on_global_mouse_click(self, x, y, button, pressed):
        button_state.update(button, pressed)

    def setup_tray(self):
        try:
            import pystray
            icon_img = Image.new('RGB', (64, 64), color='gray')
            menu = pystray.Menu(
                pystray.MenuItem("Show", self.show_window),
                pystray.MenuItem("Exit", self.exit_app)
            )
            self.tray_icon = pystray.Icon("macro_assistant", icon_img, APP_NAME, menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
        except ImportError:
            self.horse_speak("pystray not installed; tray disabled")

    def minimize_to_tray(self):
        if self.tray_icon:
            self.withdraw()
        else:
            self.destroy()

    def show_window(self):
        self.deiconify()
        self.lift()

    def toggle_stealth(self):
        if self.stealth:
            self.show_window()
            if self.tray_icon:
                self.tray_icon.visible = True
            self.stealth = False
            self.horse_speak("Stealth mode OFF")
        else:
            self.withdraw()
            if self.tray_icon:
                self.tray_icon.visible = False
            self.stealth = True
            self.horse_speak("Stealth mode ON")

    def exit_app(self):
        global recoil_running, rapid_running
        recoil_running = False
        rapid_running = False
        self.save_app_settings()
        self.quit()
        sys.exit(0)

    def on_closing(self):
        self.minimize_to_tray()

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    app = MacroApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()