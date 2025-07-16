# utils/buttons.py

from telethon import Button

def get_control_buttons():
    return [
        [
            Button.inline("⏪ SeekBack", data="seekback"),
            Button.inline("⏩ Seek", data="seek"),
        ]
    ]
