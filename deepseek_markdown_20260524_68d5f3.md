# 🎮 i_am_bad_at_games v1.0

**Recoil & Rapid Fire Macro Assistant** – a modern, always‑on‑top GUI tool for Windows that helps you compensate recoil and add rapid fire in games. Built with Python, `customtkinter`, and `pynput`.

![Screenshot Placeholder](https://via.placeholder.com/800x450?text=Macro+Assistant+UI)

## ✨ Features

- **Recoil Macro** – Adjust vertical (-10 … +10) and horizontal (-2.5 … +2.5) compensation with **0.1‑step precision**.  
- **Rapid Fire Macro** – Automatic mouse clicking while holding a key or mouse button. Adjustable click interval (0.01–0.5 s).  
- **Activation Modes**  
  - Recoil: LMB only or RMB+LMB simultaneously.  
  - Rapid Fire: keyboard key **or** mouse button (left, right, middle, X1, X2).  
- **Global Hotkeys** (work even when the window is not focused)  
  - `F1` – toggle Recoil Macro on/off  
  - `F3` – toggle Rapid Fire on/off  
  - `F10` – quick‑save current settings as a preset  
  - `Insert` – toggle stealth mode (hide/show window)  
- **Preset System** – save/load/delete named presets. The last used preset is automatically loaded on startup.  
- **Always on Top** – window stays above games and other applications.  
- **System Tray** – minimise to tray, restore, or exit.  
- **Dark Modern UI** – collapsible cards, sidebar navigation, neon accents.

## 📦 Requirements

- Windows 10 / 11 (the macro uses `ctypes` for mouse input, but the UI works on any OS – macros are Windows‑only)  
- Python 3.8 or newer

## 🔧 Installation

1. **Clone or download** this repository.

2. **Install the required Python packages** (preferably in a virtual environment):
   ```bash
   pip install customtkinter pynput pillow