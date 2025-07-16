# utils/buttons.py

from telethon import Button

def get_playback_buttons():
    return [
        [
            Button.inline("⏪ SeekBack", data="seekback"),
            Button.inline("⏸ Pause", data="pause"),
            Button.inline("⏩ Seek", data="seek")
        ],
        [
            Button.inline("🔁 Resume", data="resume"),
            Button.inline("❌ Close", data="close")
        ]
    ]

def get_start_buttons():
    return [
        [Button.inline("📜 Help", data="show_help")]
    ]
