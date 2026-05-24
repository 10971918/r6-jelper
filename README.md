@ How to Use
Recoil Macro

    Switch to the Recoil tab.

    Adjust the sliders:

        Vertical – how many pixels down (positive) or up (negative) per shot.

        Horizontal – left/right drift compensation.

        Sensitivity – global multiplier.

        Sleep Time – delay between recoil moves (lower = faster).

        First Shot Delay – extra delay before the first recoil move.

        Legit Mode – adds random jitter to avoid detection.

        Randomization – max additional random pixels.

    Choose Activation Mode: LMB (hold left mouse button) or RMB+LMB (hold both).

    Press F1 to arm the macro (status turns green). Hold the selected mouse button(s) while shooting – the cursor will move automatically.

Rapid Fire Macro

    Switch to the Rapid Fire tab.

    Select Activation Type: key or mouse.

        For key: click “Select Key” and press any key (letter, number, function key, space, etc.).

        For mouse: choose a button from the dropdown (left, right, middle, X1, X2).

    Set the Click Interval – lower values give faster firing.

    Press F3 to arm Rapid Fire. While holding the selected key or mouse button, the macro will repeatedly click your left mouse button.

Presets (Save / Load)

    Switch to the Settings tab.

    Enter a name in the Preset Name field and click Save – all current recoil + rapid fire settings are stored.

    To load a preset, select it from the dropdown and click Load.

    Use Delete to remove a preset.

    Click Open Presets Folder to access the presets.json file directly – you can share it between computers.

Quick‑Save with F10

Press F10 at any time – a dialog will ask for a preset name. The current settings are saved instantly (same as using the Settings tab).
Stealth Mode

Press Insert to hide the window completely (system tray icon also disappears). Press Insert again to bring it back.
🗂️ Files & Storage

All data is stored in your user folder:
text

%USERPROFILE%\.macro_assistant\
├── presets.json          # your saved presets
├── app_settings.json     # last used preset (auto‑loaded)
└── macro_log.txt         # debug log (if something goes wrong)

You can copy presets.json to another PC – the script will load it from the same relative path.
⚠️ Troubleshooting

    The macro doesn’t move the mouse
    Make sure you are running the script as Administrator (Windows requires admin rights for simulated mouse input in some games).

    Rapid fire key selection crashes
    This has been fixed. Use the “Select Key” button – it runs in a separate thread and won’t freeze the UI.

    Middle mouse button not working
    It works if you select middle from the mouse button dropdown. Ensure your game doesn’t block the input.

    UnicodeEncodeError when logging
    The log file is opened with utf-8 encoding – no more crashes.

    Presets not loading automatically
    Check that app_settings.json exists and contains a valid preset name. The script silently falls back to default settings.

🛠️ Building an Executable (optional)

If you want a standalone .exe file (no Python required), use PyInstaller:

bash
###########################################
pip install pyinstaller
pyinstaller --onefile --windowed --name "MacroAssistant" macro_assistant.py
###########################################

This project is provided for educational purposes only. Use it at your own risk. The author is not responsible for any bans or damages caused by improper use.

Enjoy fragging with less recoil and faster clicks!
Made with ❤️ for gamers who are a little bad at games.
